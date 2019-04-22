FROM dit-sonar-img:7.5

#Config sonarqube
COPY --chown=sonarqube:sonarqube plugins/sonar-findbugs-plugin-3.9.3.jar /opt/sonarqube/extensions/plugins
COPY --chown=sonarqube:sonarqube plugins/sonar-pmd-plugin-3.2.0.jar /opt/sonarqube/extensions/plugins    
COPY --chown=sonarqube:sonarqube plugins/checkstyle-sonar-plugin-4.18.jar /opt/sonarqube/extensions/plugins 

WORKDIR $SONARQUBE_HOME
COPY --chown=sonarqube:sonarqube profiles/java-git-qualityprofile.xml $SONARQUBE_HOME/bin
COPY --chown=sonarqube:sonarqube scripts/start_with_profile.sh $SONARQUBE_HOME/bin/
COPY --chown=sonarqube:sonarqube scripts/post_config_sonar.py $SONARQUBE_HOME/bin/
COPY --chown=sonarqube:sonarqube config/sonar.properties $SONARQUBE_HOME/conf

#Set up sonarqube entrypoint with postprocessing script inside
USER sonarqube
ENTRYPOINT ["bash", "./bin/start_with_profile.sh"]

#Config python for using in postprocessing script
USER root
ENV PYTHON_PIP_VERSION 19.0.3
RUN set -ex; \
	\
	wget -O get-pip.py 'https://bootstrap.pypa.io/get-pip.py'; \
	\
	python get-pip.py \
		--disable-pip-version-check \
		--no-cache-dir \
		"pip==$PYTHON_PIP_VERSION" \
	; \
	pip --version; \
	\
	find /usr/local -depth \
		\( \
			\( -type d -a \( -name test -o -name tests \) \) \
			-o \
			\( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \
		\) -exec rm -rf '{}' +; \
	rm -f get-pip.py
RUN pip install requests
