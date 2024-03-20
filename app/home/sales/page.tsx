import React from "react";
import Navbar from "@/app/components/Navbar";
import CashSale from "@/app/components/CashSale";

const Sales = () => {
  return (
    <div className="flex min-h-screen">
      <Navbar />
      <div className="flex-1 mt-10 px-4">
        <CashSale />
      </div>
    </div>
  );
};

export default Sales;
