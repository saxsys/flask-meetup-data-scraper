FROM traefik:v2.1.3
RUN mkdir -p /etc/traefik/acme
RUN touch /etc/traefik/acme/acme.json
RUN chmod 600 /etc/traefik/acme/acme.json
COPY ./compose/production/traefik/traefik.yml /etc/traefik

# add basic auth
COPY ./compose/production/traefik/basic-auth-usersfile /basic-auth-usersfile
