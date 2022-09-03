FROM registry.fedoraproject.org/f33/python3
# Add application sources to a directory that the assemble script expects them
# and set permissions so that the container runs without root access
USER 0
##COPY . /tmp/src
RUN git clone http://ZZ000C:2qkXrU-qVb6f2aJypgQL@10.11.4.66/python_projects/pvx-iit-srvc.git /tmp/src -b tz-000001-init
RUN /usr/bin/fix-permissions /tmp/src
USER 1001

# Install the dependencies
RUN python3.9 -m pip install --upgrade pip
RUN /usr/libexec/s2i/assemble
EXPOSE 8080
EXPOSE 5000
# Set the default command for the resulting image
CMD /usr/libexec/s2i/run
