const express = require("express");
const app = express();

app.get("/secret", (req, res) => res.send("Hello World!"));

app.listen(3000, () => console.log("Server listening on port 3000!"));
