import ThemeSwitcher from "./ThemeSwitcher";
import Navbar from "./Navbar";

function App() {
  return (
    <div>
      <Navbar />
      <div className="App min-vh-100 d-flex justify-content-center align-items-center">
        <ThemeSwitcher />
      </div>
    </div>
  );
}

export default App;