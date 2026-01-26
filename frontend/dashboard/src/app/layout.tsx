import { Montserrat } from "next/font/google";
import "./globals.css";
import "flatpickr/dist/flatpickr.css";

const montserrat = Montserrat({
  subsets: ["latin", "cyrillic"],
  weight: ["400", "500", "600", "700"],
  display: "swap",
});

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ru">
      <body className={`${montserrat.className} bg-gray-50`}>
        {children}
      </body>
    </html>
  );
}
