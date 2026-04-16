import { Link } from "react-router-dom";

// Mock de categorias
const categories = [
    {
        id: 1,
        name: "Bolos Decorados",
        slug: "bolos-decorados",
        description: "Bolos personalizados para todas as ocasiões.",
        image: "/assets/images/categoria-bolos.jpg"
    },
    {
        id: 2,
        name: "Bolos com cobertura",
        slug: "bolos-com-cobertura",
        description: "Bolos com diferentes tipos de cobertura para todos os gostos.",
        image: "/assets/images/categoria-doces.jpg"
    },
    {
        id: 3,
        name: "Bolos da vovó",
        slug: "bolos-da-vovo",
        description: "Bolos caseiros e tradicionais.",
        image: "/assets/images/categoria-bolos-da-vovo.jpg"
    },
    {
        id: 4,
        name: "Doces e Sobremesas",
        slug: "doces-e-sobremesas",
        description: "Sobremesas individuais deliciosas para qualquer ocasião.",
        image: "/assets/images/categoria-sobremesas.jpg"
    },
    {
        id: 5,
        name: "Sobremesas Tamanho Família",
        slug: "sobremesas-tamanho-familia",
        description: "Sobremesas deliciosas em porções maiores para compartilhar com a família.",
        image: "/assets/images/categoria-tematicos.jpg"
    },
    {
        id: 6,
        name: "Bolos de pote",
        slug: "bolos-de-pote",
        description: "Bolos deliciosos em potes individuais para qualquer ocasião.",
        image: "/assets/images/categoria-bolos-de-pote.jpg"
    },
    {
        id: 7,
        name: "Cones recheados",
        slug: "cones-recheados",
        description: "Cones deliciosos recheados para qualquer ocasião.",
        image: "/assets/images/categoria-cones-recheados.jpg"
    },
    {
        id: 8,
        name: "Copos da felicidade",
        slug: "copos-da-felicidade",
        description: "Copos deliciosos recheados para qualquer ocasião.",
        image: "/assets/images/categoria-copos-da-felicidade.jpg"
    },
    
];

export default function CategoryCards() {
    return (
        <section className="py-10 w-full">
            <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">Categorias</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
                {categories.map((cat) => (
                    <Link
                        key={cat.id}
                        to={`/cardapio/${cat.slug}`}
                        className="category-card"
                    >
                        <img
                            src={cat.image}
                            alt={cat.name}
                            className="category-card-img"
                        />
                        <div className="category-card-content">
                            <h3 className="category-card-title">{cat.name}</h3>
                            <p className="category-card-desc">{cat.description}</p>
                            <span className="category-card-btn">Ver produtos</span>
                        </div>
                    </Link>
                ))}
            </div>
        </section>
    );
}
