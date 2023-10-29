const express = require('express');
const axios = require('axios');
const dotenv = require('dotenv');

dotenv.config();
const app = express();
const PORT = 3000;

app.use(express.json());

const cors = require('cors');

app.use(cors());


app.post('/generate-math-question', async (req, res) => {
    const difficulty = req.body.difficulty;

    const prompt = `Generate a ${difficulty} math question for elementary school students:`;

    try {
        const response = await axios.post('https://api.openai.com/v1/engines/davinci/completions', {
            prompt: prompt,
            max_tokens: 100
        }, {
            headers: {
                'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
                'Content-Type': 'application/json'
            }
        });

        res.json(response.data.choices[0].text.trim());
    } catch (error) {
        res.status(500).json({ error: "Failed to fetch question from OpenAI" });
    }
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
