docker_run:
	# docker build -t llm_anime_recommendation:latest . && \
	# docker run --gpus all -it -v ${PWD}:/app llm_anime_recommendation:latest /bin/bash
	docker build -t langchain_ambai:latest . && \
	docker run --gpus all -it -v ${PWD}:/app langchain_ambai:latest /bin/bash
