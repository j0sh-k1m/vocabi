import "./App.css";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";

const loggedIn = true;

function App() {
  return (
    <>
      {loggedIn ? <HomePage></HomePage> : <LoginPage></LoginPage>}
    </>
  );
}

export default App;
