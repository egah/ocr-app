mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"egahepiphane@gmail.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml

sudo apt install tesseract-ocr -y
sudo apt install tesseract-ocr-eng -y