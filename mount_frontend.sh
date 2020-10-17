# this script builds the frontend app and mounts it into
# the `static/` directory in the server

# prerequisites: npm is in PATH

cd frontend \
&& npm install \
&& npm run build \
&& cd .. \
&& rm -rf server/static/* \
&& cp -r frontend/public/* server/static/ \