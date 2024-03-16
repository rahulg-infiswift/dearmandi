import Navbar from "@/app/components/Navbar";
import IncomeStatement from "@/app/components/IncomeStatement";

const Report = () => (
  <div className="flex">
    <Navbar />
    <div className="flex-grow max-w-4xl mx-auto mt-10 px-4 sm:px-6 lg:px-8">
      <IncomeStatement />
    </div>
  </div>
);

export default Report;
