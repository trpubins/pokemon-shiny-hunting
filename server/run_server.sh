# launch the server
cd $POKEMON_PROJ_PATH/server && \
    $POKEMON_PROJ_PATH/.venv/bin/uvicorn \
    server:app \
    --host 0.0.0.0 \
    --port 8000 \
    &  # tells bash to run this command in a separate process
