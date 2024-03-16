import React from "react";
import Navbar from "@/app/components/Navbar";
import CashPurchase from "@/app/components/CashPurchase";

const Purchases = () => {
  return (
    <div className="flex">
      <Navbar />
      <div className="flex-grow max-w-4xl mx-auto mt-10 px-4 sm:px-6 lg:px-8">
        <CashPurchase />
      </div>
    </div>
  );
};

export default Purchases;
