/** Legacy footer — Layout.tsx ships the live colophon. */
export default function Footer() {
  return (
    <footer className="colophon">
      <span>Sticker Shop · print studio</span>
      <span>© {new Date().getFullYear()}</span>
    </footer>
  );
}
