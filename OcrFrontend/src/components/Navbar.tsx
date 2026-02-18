import { ScanText } from "lucide-react";
import { ThemeToggle } from "./ThemeToggle";

export function Navbar() {
  const handleNavbarClick = (e: React.MouseEvent) => {
    // Prevent navbar clicks from propagating to parent elements
    e.stopPropagation();
  };

  const handleImageError = (e: React.SyntheticEvent<HTMLImageElement, Event>) => {
    // Fallback: hide broken image and show icon instead
    e.currentTarget.style.display = "none";
    const fallback = e.currentTarget.nextElementSibling as HTMLElement;
    if (fallback) {
      fallback.style.display = "block";
    }
  };

  return (
    <nav
      className="h-14 border-b flex items-center justify-between px-6 bg-background"
      onClick={handleNavbarClick}
    >
      <div className="flex items-center">
        <img
          src="/logo.svg"
          alt="Infotextify logo"
          width={20}
          height={20}
          className="mr-2"
          onError={handleImageError}
          loading="eager"
        />
        <ScanText
          className="h-5 w-5 mr-2 text-primary hidden"
          aria-hidden="true"
        />
        <h1 className="text-lg font-semibold">Infotextify</h1>
      </div>
      <ThemeToggle />
    </nav>
  );
}
