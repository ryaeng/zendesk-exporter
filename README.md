# Zendesk Exporter

Data is boring. This may ruffle some feathers, but I believe it to be true. At least... until I
started working with the visualization of data. Graphs brought data to life for me. It gave me
eyes to see, literally, and beagan to fuel a fire in me. The fire that burns is the desire to
use data in a way which helps myself and others discover problem sooner.

Will be discover problems sooner, most certainly. This may even help us uncover problems that
we didn't even know we had.


## How does it work?

We start by defining a Prometheus metric(s). We then reach out to Zendesk's API to grab data from
whichever endpoint we choose, e.g. tickets, groups, etc. Once we have the data we want, we may
manipulate that data however we choose. That data will then be returned using the Prometheius
metric(s) we created initially.

The visualization of this data requires that Prometheus & Grafana be configured separately.

*Note: Docker compose is used as a part of this project to include the local setup of Prometheus & 
Grafana. There intended use here is to make local dev & visualization easier.*


## How do I run this setup?

Move into this directory and run `docker compose up`. You may also include the -d option in the event
you'd like to detach the container from your console. This will prevent your console from filling up with output from the container.
```
cd zendesk-exporter
docker compose up [-d]
```


## How do I access Prometheus locally?

Once you've started the containsers using `docker compose`, you'll be able to access Prometheus by
navigating to http://localhost:9000. The credentials are admin/admin.

*Note: Visualizations haven't yet been setup in Grafana. I'm still working on getting hte metrics
configured properly in Prometheus.*
