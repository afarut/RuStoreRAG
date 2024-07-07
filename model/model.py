from transformers import logging

logging.set_verbosity_error()
import warnings

warnings.filterwarnings('ignore')
from sentence_transformers import SentenceTransformer
from sentence_transformers.models import Pooling, Transformer
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from qdrant_client import QdrantClient

PROMPT_TEMP = '''system
Ты — Сайга, русскоязычный автоматический ассистент. Ты разговариваешь с людьми и помогаешь им.user
Используй только следующий контекст, чтобы ответить на вопрос в конце. Если ты не знаешь ответа напиши "Ответ не найден". Не пытайся выдумывать ответ.
Контекст:
###
{chunks_join}
###
Вопрос:
###
{query}assistant'''

text_temp = '''Путь до страницы: {path}
{chunk}
'''

encoder_name = 'intfloat/multilingual-e5-large'
chunk_size = 1800
n_top_cos = 2
join_sym = '\n---\n'

hyper_params = {"max_new_tokens": 558,
                "temperature": 0.41568222794150655,
                "top_p": 0.6273831810298036,
                "top_k": 89}

model_id = 'IlyaGusev/saiga_llama3_8b'

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map='auto'
)
# Создание подключения к векторной базе данных Qdrant
qdrant_client = QdrantClient('80.242.58.249', port=6333, timeout=60)


# Функция для получения би-энкодера и его размерности
def get_bi_encoder(bi_encoder_name):
    raw_model = Transformer(model_name_or_path=f'{bi_encoder_name}')
    bi_encoder_dim = raw_model.get_word_embedding_dimension()
    pooling_model = Pooling(
        bi_encoder_dim,
        pooling_mode_cls_token=False,
        pooling_mode_mean_tokens=True
    )
    bi_encoder = SentenceTransformer(
        modules=[raw_model, pooling_model],
        device='cuda'  # Использование устройства CUDA
    )
    return bi_encoder, bi_encoder_dim


# Функция для преобразования текста в вектор с помощью би-энкодера
def str_to_vec(bi_encoder, text):
    embeddings = bi_encoder.encode(
        text,
        convert_to_tensor=True,
        show_progress_bar=False
    )
    return embeddings


# Функция для поиска похожих векторов в коллекции Qdrant
def vec_search(bi_encoder, encoder_name, query, n_top_cos, chunk_size):
    COLL_NAME = f'rstr_{encoder_name.replace("/", "_")}_{chunk_size}'
    query_emb = str_to_vec(bi_encoder, query)
    search_result = qdrant_client.search(
        collection_name=COLL_NAME,
        query_vector=query_emb,
        limit=n_top_cos,
        with_vectors=False
    )

    top_chunk = [x.payload['chunk'] for x in search_result]
    top_url = [x.payload['url'] for x in search_result]
    top_path = [x.payload['path'] for x in search_result]
    return top_chunk, top_url, top_path


# Функция для получения ответа модели LLM на основе запроса и контекста
def get_llm_answer(prompt_temp, query, chunks_join, **hyper_params):
    prompt = prompt_temp.format(chunks_join=chunks_join, query=query)

    def generate(model, tokenizer, prompt):
        data = tokenizer(prompt, return_tensors="pt", add_special_tokens=False)
        data = {k: v.to(model.device) for k, v in data.items()}
        output_ids = model.generate(
            **data,
            **hyper_params,
            bos_token_id=128000,
            eos_token_id=128009,
            pad_token_id=128000,
            do_sample=True,
            no_repeat_ngram_size=15,
            repetition_penalty=1.12,
        )[0]
        output_ids = output_ids[len(data["input_ids"][0]):]
        output = tokenizer.decode(output_ids, skip_special_tokens=True)
        return output.strip()

    response = generate(model, tokenizer, prompt)
    return response


# Главная функция для получения ответа на запрос
def get_answer(query):
    bi_encoder, vec_size = get_bi_encoder(encoder_name)
    top_chunk, top_url, top_path = vec_search(bi_encoder, encoder_name, query, n_top_cos, chunk_size)
    chunks = [text_temp.format(path=pt, chunk=ch) for pt, ch in zip(top_path, top_chunk)]
    chunks_join = join_sym.join(chunks)
    answer = get_llm_answer(PROMPT_TEMP, query, chunks_join, **hyper_params)
    return answer


if __name__ == "__main__":
    print(get_answer("Это всего-то тестовый запрос"))
