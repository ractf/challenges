FROM docker.io/grafana/grafana
ENV GF_INSTALL_PLUGINS=frser-sqlite-datasource
ADD datasource.yaml /etc/grafana/provisioning/datasources/datasource.yaml
#ADD dashboard.yaml /etc/grafana/provisioning/dashboards/dashboard.yaml
ADD grafana.ini /etc/grafana/grafana.ini
ADD ractf.json /app/dashboards/ractf.json
ADD --chown=root:root data.db /app/data.db
