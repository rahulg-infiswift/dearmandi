"use client";
import Link from "next/link";
import React from "react";
import { HomeIcon, UserPlusIcon, BanknotesIcon, CurrencyRupeeIcon, BookOpenIcon, QuestionMarkCircleIcon } from "@heroicons/react/24/outline";

export default function Navbar() {
  return (
    <div
      className="fixed top-0 left-0 h-full bg-gray-100 text-white shadow-md z-50 w-1/5"
    >
      <div className="px-4 py-4 flex flex-col">
        <div className="mb-8 flex flex-grow items-center justify-center">
          <h1 className="text-3xl font-bold text-black text-center">
            DEARmandi
          </h1>
        </div>
        <nav className="flex flex-col space-y-5">
          <div className="flex justify-center items-center bg-gray-800 hover:bg-gray-900 p-4 rounded-lg ">
            <Link
              href="/"
              className="flex justify-center items-center text-lg  transition-colors duration-300"
            >
              <HomeIcon className="w-6 mb-1 mr-2" />
              Home
            </Link>
          </div>
          <div className="flex justify-center items-center bg-gray-800 hover:bg-gray-900 p-4 rounded-lg ">
            <Link
              href="/home/create_entity"
              className="flex justify-center items-center text-lg hover:text-gray-300 transition-colors duration-300"
            >
              <UserPlusIcon className="w-6 mb-1 mr-2" />
              Register
            </Link>
          </div>
          <div className="flex justify-center items-center bg-gray-800 hover:bg-gray-900 p-4 rounded-lg ">
            <Link
              href="/home/purchases"
              className="flex justify-center items-center text-lg hover:text-gray-300 transition-colors duration-300"
            >
              <BanknotesIcon className="w-6 mb-1 mr-2" />
              Purchases
            </Link>
          </div>
          <div className="flex justify-center items-center bg-gray-800 hover:bg-gray-900 p-4 rounded-lg ">
            <Link
              href="/home/sales"
              className="flex justify-center items-center text-lg hover:text-gray-300 transition-colors duration-300"
            >
              <CurrencyRupeeIcon className="w-6 mb-1 mr-2" />
              Sales
            </Link>
          </div>
          <div className="flex justify-center items-center bg-gray-800 hover:bg-gray-900 p-4 rounded-lg ">
            <Link
              href="/home/report"
              className="flex justify-center items-center text-lg hover:text-gray-300 transition-colors duration-300"
            >
              <BookOpenIcon className="w-6 mb-1 mr-2" />
              Report
            </Link>
          </div>
          <div className="flex justify-center items-center bg-gray-800 hover:bg-gray-900 p-4 rounded-lg ">
            <Link
              href="/home/faqs"
              className="flex justify-center items-center text-lg hover:text-gray-300 transition-colors duration-300"
            >
              <QuestionMarkCircleIcon className="w-6 mb-1 mr-2" />
              FAQs
            </Link>
          </div>
        </nav>
      </div>
    </div>
  );
}
