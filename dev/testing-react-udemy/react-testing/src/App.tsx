import React, { useEffect, useState } from "react";
import "./App.css";
import { User, getUser } from "./get-user";
import CustomInput from "./CustomInput";

function App() {
  const [text, setText] = useState("");
  const [ user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const fetchUser = async() => {
      const user = await getUser();
      setUser(user)
    }

    fetchUser();
  }, [])

  function handleChange(event: React.ChangeEvent<HTMLInputElement>) {
    setText(event.target.value);
  }

  return (
    <div>
    {user ? <p>Username: {user.name}</p> : null}
    <CustomInput value={text} onChange={handleChange}>
      Input:
    </CustomInput>
    <p>You typed: {text ? text : "..."} </p>
    </div>
  );
}



export default App;
