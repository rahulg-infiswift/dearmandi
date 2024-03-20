"use client";
import Link from "next/link";
import React from "react";
import {
  HomeIcon,
  UserPlusIcon,
  BanknotesIcon,
  CurrencyRupeeIcon,
  BookOpenIcon,
  QuestionMarkCircleIcon,
} from "@heroicons/react/24/outline";

export default function Navbar() {
  return (
    <div className="flex flex-col w-1/5 top-0 px-6 py-8 left-0 bg-gray-900 text-white shadow-md z-10 p-4">
      <h1 className="flex justify-center text-xl pb-8 md:text-2xl lg:text-4xl font-bold text-white text-center truncate">
        DEARmandi
      </h1>
      <nav className="flex-1 space-y-4">
      <div className="flex justify-center items-center bg-gray-800 hover:bg-gray-900 p-4 rounded-lg ">
          <Link
            href="/"
            className="flex justify-center items-center text-lg hover:text-gray-300 transition-colors duration-300"
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
  );
}
