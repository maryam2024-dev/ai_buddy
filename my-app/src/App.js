import './App.css';
import Splash from "./components/Splash";
import "@fontsource/roboto";
import SignUp from "./components/signUp";
import Home from "./components/Home";
import Alphabet from "./components/alphabet"; // Defaults to weight 400
import AlphabetEn from "./components/alphabetEn";
import NotFound from "./components/NotFound";
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import SignIn from "./components/signIn";
import Story from "./components/story";
import Evaluation from "./components/evaluation";

function App() {
  return (
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Splash />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="/signin" element={<SignIn />} />
          <Route path="/home" element={<Home />} />
          <Route path="/alphabet-ar" element={<Alphabet />} />
          <Route path="/alphabet-en" element={<AlphabetEn />} />
          <Route path="/story" element={<Story />} />
          <Route path="/eval" element={<Evaluation />} />
          <Route path="*" element={<NotFound />} /> {/* Catch-all route for 404 pages */}
        </Routes>
      </BrowserRouter>
  );
}

export default App;
