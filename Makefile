test:
	coverage run setup.py test
test-report:
	coverage report -m
update_swagger_codegen:
	mvn dependency:get -Dartifact=io.swagger:swagger-codegen-cli:2.2.3:jar -DremoteRepositories=central::default::https://repo.maven.apache.org/maven2
	pushd datadotworld/client; \
	curl https://api.data.world/v0/swagger.json -o swagger-dwapi-def.json; \
	java -jar ~/.m2/repository/io/swagger/swagger-codegen-cli/2.2.3/swagger-codegen-cli-2.2.3.jar generate -l python --git-repo-id=data.world-py --git-user-id=datadotworld \
		--http-user-agent="data.world-py" --invoker-package=client \
		-i swagger-dwapi-def.json -c swagger-codegen-config.json --release-note=""; \
	popd;