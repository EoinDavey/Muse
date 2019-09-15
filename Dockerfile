from angular/ngcontainer
RUN npm i -g @angular/cli
COPY . .
WORKDIR Clio/
RUN sudo npm i
