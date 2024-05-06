import Navbar from "@/components/Navbar";
import { ThreeDCardDemo } from "@/components/cards";
import Image from "next/image";

export default function Home() {
  return (
    <div className="m-5">
      <Navbar />
      <div className="flex flex-wrap justify-between">
        <ThreeDCardDemo
          title="Unir PDF"
          description="Unir dos o mas pdfs sin perder calidad"
          image="/UnirPdf.png"
          link="/unir"
        />
        <ThreeDCardDemo
          title="Comprimir PDF"
          description="Comprimir PDFs sin perder calidad"
          image="/ComprimirPdf.png"
          link="/comprimir"
        />
        <ThreeDCardDemo
          title="Separar PDF"
          description="separar PDFs sin perder calidad"
          image="/SepararPdf.png"
          link="/separar"
        />
      </div>
    </div>
  );
}
