mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \egahepiphane@gmail.com"\n\
\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml