import Header from "./Header";

export default function Layout({ children }) {
    return (
        <div className="layout">
            <Header />
            <main className="layout__main">{children}</main>
        </div>
    );
}
