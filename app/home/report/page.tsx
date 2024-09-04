import Navbar from "@/app/components/Navbar";
import IncomeStatement from "@/app/components/IncomeStatement";

const Report = () => (
  <div className="flex min-h-screen">
    <Navbar />
    <div className="flex-auto">
      <IncomeStatement />
    </div>
  </div>
);

export default Report;
