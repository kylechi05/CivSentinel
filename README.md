## Tasks
#### Frontend - Next.js, TailwindCSS, Leaflet.js, deploeyd on Vercel
- [ ] Make app
#### Database - Supabase
- [x] Seed database with remote stored procedures and init data
- [ ] Create triggers for scraper data
#### Web Scraper - Requests, BeautifulSoup4, Supabase
- [x] Create scraper
- [x] Connect scraper to Supabase
- [ ] Consume Kafka scraper pings
#### Queue Pipeline - Kafka
- [x] Setup Kafka
- [x] Create Topics
- [ ] Create Scraper pinger
#### DL model - Python, PyTorch, SpatioTemporal GNN
- [ ] Train model
- [ ] Deploy model
#### Data Caching - Redis
#### Containers - Docker, Kubernetes
- [x] Containerize each service built
- [x] Use docker compose for local development
- [ ] Experiment with K8s minikube
#### Backend Deployed on Fly.io/Render
- [ ] Not sure if backend will be deployed - hard to find free k8s deployment resources

# Thougths
train model on chicago dataset, use transfer learning
scrape iowa city arrest blotter / uiowa crime log every 30 seconds
send data scrapped into kafka queueing system before prediction
use data in model prediction, update supabase with new data
pull data from supabase and cache it in redis
use data in frontend and map with leaflet.js
