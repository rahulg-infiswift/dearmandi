import React from "react";
import CashPurchase from "@/src/components/CashPurchase";

const Purchases = () => {
  return (
    <div className="flex min-h-screen">
      <div className="flex-auto mt-10 px-4">
        <CashPurchase />
      </div>
    </div>
  );
};

export default Purchases;
