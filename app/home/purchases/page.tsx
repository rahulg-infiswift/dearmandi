import React from "react";
import Navbar from "@/app/components/Navbar"; // Adjust the import path according to your project structure

export default function PurchasingSection() {
  const headers = [
    "Kisan Name",
    "Crop Name",
    "Quantity",
    "Total Weight",
    "Price",
  ];

  return (
    <div className="flex min-h-screen">
      <Navbar />
      <div className="flex-1 p-4 ml-[16rem]">
        {" "}
        {/* Adjust ml-[16rem] based on your Navbar's actual width */}
        <h1 className="text-xl font-bold mb-4">Purchasing Section</h1>
        <div className="overflow-x-auto">
          <table className="min-w-full leading-normal">
            <thead>
              <tr>
                {headers.map((header, index) => (
                  <th
                    key={index}
                    className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider"
                  >
                    {header}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              <tr>
                <td
                  colSpan={headers.length}
                  className="px-5 py-5 border-b border-gray-200 bg-white text-sm"
                >
                  <p className="text-gray-900 whitespace-no-wrap text-center">
                    No sales data available.
                  </p>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
