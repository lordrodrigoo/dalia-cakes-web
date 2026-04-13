from uuid import uuid4
from typing import Optional

from backend.src.config.settings import settings
from backend.src.domain.repositories.product_repository import ProductRepositoryInterface
from backend.src.domain.repositories.category_repository import CategoryRepositoryInterface
from backend.src.infra.gemini.gemini_client import GeminiClient
from backend.src.dto.response.chatbot_response import ChatbotResponse
from backend.src.exceptions.exception_handlers_chatbot import ChatbotUnavailableException

# In-memory conversation history: { session_id: [{"role": ..., "parts": [...]}] }
_chat_history: dict[str, list[dict]] = {}


class ChatbotUsecase:
    def __init__(
        self,
        product_repository: ProductRepositoryInterface,
        category_repository: CategoryRepositoryInterface,
        gemini_client: GeminiClient,
    ):
        self.product_repository = product_repository
        self.category_repository = category_repository
        self.gemini_client = gemini_client

    def chat(self, message: str, session_id: Optional[str] = None) -> ChatbotResponse:
        if not session_id:
            session_id = str(uuid4())

        history = _chat_history.get(session_id, [])
        system_prompt = self._build_system_prompt()

        try:
            reply = self.gemini_client.send_message(
                message=message,
                history=history,
                system_prompt=system_prompt,
            )
        except Exception as exc:
            raise ChatbotUnavailableException() from exc

        history = history + [
            {"role": "user", "parts": [{"text": message}]},
            {"role": "model", "parts": [{"text": reply}]},
        ]

        max_entries = settings.CHATBOT_MAX_HISTORY * 2
        if len(history) > max_entries:
            history = history[-max_entries:]

        _chat_history[session_id] = history

        return ChatbotResponse(reply=reply, session_id=session_id)

    def _build_system_prompt(self) -> str:
        categories = self.category_repository.get_all_categories()
        products = self.product_repository.get_all_products()

        categories_text = ", ".join(c.name for c in categories) if categories else "não informado"
        products_text = (
            "\n".join(f"- {p.name}: R$ {p.price:.2f}" for p in products)
            if products
            else "Consulte diretamente pelo WhatsApp."
        )

        return (
            f"Você é um assistente virtual simpático da confeitaria {settings.BUSINESS_NAME}.\n\n"
            f"Informações do negócio:\n"
            f"- Endereço: {settings.BUSINESS_ADDRESS}, {settings.BUSINESS_CITY}\n"
            f"- Horário de funcionamento: {settings.BUSINESS_HOURS}\n"
            f"- WhatsApp (encomendas): {settings.BUSINESS_PHONE}\n"
            f"- iFood: {settings.BUSINESS_IFOOD_LINK}\n"
            f"- Formas de pagamento: {settings.BUSINESS_PAYMENT_METHODS}\n"
            f"- Site de receitas: {settings.BUSINESS_RECIPES_URL}\n\n"
            f"Bolos decorados:\n"
            f"- Preço médio: R$ {settings.BUSINESS_CAKE_PRICE_PER_KG}/kg\n"
            f'- Para bolos personalizados, o cliente deve entrar em contato para orçamento\n'
            f"- Pedidos com antecedência de: {settings.BUSINESS_ORDER_ADVANCE_DAYS}\n\n"
            f"Categorias disponíveis: {categories_text}\n\n"
            f"Produtos e preços:\n{products_text}\n\n"
            f"Instruções importantes:\n"
            f"- Seja simpático, acolhedor e use o nome da confeitaria com carinho\n"
            f"- Responda sempre em português\n"
            f"- Para encomendas, direcione ao WhatsApp: {settings.BUSINESS_PHONE}\n"
            f"- Para pedidos online, sugira o iFood: {settings.BUSINESS_IFOOD_LINK}\n"
            f"- Para receitas, indique: {settings.BUSINESS_RECIPES_URL}\n"
            f"- Mantenha respostas curtas e objetivas\n"
            f"- Não invente informações não fornecidas acima\n"
            f"- Só trabalhamos com ifood e encomendas via WhatsApp, não oferecemos vendas diretas pelo site\n"
            f"- Se não souber a resposta, seja honesto e sugira entrar em contato pelo WhatsApp para mais detalhes\n"
            f"- Trabalhamos de portas fechadas e não atendemos presencialmente, todas as vendas são online ou por telefone\n"
        )
