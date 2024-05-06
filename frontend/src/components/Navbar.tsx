import React from "react";
import { FaRegFilePdf } from "react-icons/fa6";

const Navbar = () => {
  return (
    <div className="p-2 md:p-10 flex items-center justify-between">
      <div className="flex items-center">
        <FaRegFilePdf size={40} />
        <h1 className="ml-2 text-2xl font-bold">PDF-editor</h1>
      </div>
      <div>
        <h1 className="font-bold">Dax</h1>
      </div>
    </div>
  );
};

export default Navbar;
