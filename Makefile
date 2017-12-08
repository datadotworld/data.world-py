test:
	coverage run setup.py test
test-report:
	coverage report -m
update_swagger_codegen:
	pushd datadotworld/client; \
	curl https://api.data.world/v0/swagger.json -o swagger-dwapi-def.json; \
	swagger-codegen generate -l python --git-repo-id=data.world-py --git-user-id=datadotworld \
		--http-user-agent="data.world-py" --invoker-package=client \
		-i swagger-dwapi-def.json -c swagger-codegen-config.json --release-note=""; \
	popd;
