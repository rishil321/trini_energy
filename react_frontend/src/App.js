import Navbar from "./Navbar";
import NaturalGasProductionChart from "./NaturalGasProductionChart";

function App() {
  return (
    <div>
      <Navbar />
      <div className="">
        <NaturalGasProductionChart />
      </div>
    </div>
  );
}

export default App;