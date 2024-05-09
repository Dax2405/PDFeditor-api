import Link from "next/link";
import React from "react";

const Footer = () => {
  return (
    <div>
      <div className="border"></div>
      <div>
        <nav className="px-5 items-center justify-center space-x-6">
          <Link className="hover-blue" href={"/terms"}>
            Terminos y condiciones
          </Link>
          <Link className="hover-blue" href={"https://dax-ec.ru"}>
            Dax
          </Link>
        </nav>
      </div>
    </div>
  );
};

export default Footer;
