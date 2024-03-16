import React from "react";
import Navbar from "@/app/components/Navbar";
import CashSale from "@/app/components/CashSale";

const Sales = () => {
  return (
    <div className="flex">
      <Navbar />
      <div className="flex-grow max-w-4xl mx-auto mt-10 px-4 sm:px-6 lg:px-8">
        <CashSale />
      </div>
    </div>
  );
};

export default Sales;
