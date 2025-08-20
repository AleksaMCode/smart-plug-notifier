<img width="150" align="right" src="./resources/spn_logo.png"></img>
# Smart Plug Notifier - SPN
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Python 3.10.7](https://img.shields.io/badge/python-3.10.7-blue.svg)](https://www.python.org/downloads/release/python-3107/)
![](https://img.shields.io/github/v/release/AleksaMCode/smart-plug-notifier)

<p align="justify"><b>Smart Plug Notifier</b> (SPN) is a notification system built on an asynchronous, event-driven microservices architecture. Each service runs concurrently using non-blocking operations, which ensures scalability and responsiveness.

The system is composed of two primary services:</p>
<ol>
<li><p align="justify"><b>Tapo Service</b>: responsible for monitoring Tapo smart plugs (<a href="https://www.tapo.com/en/product/smart-plug/tapo-p110/">P110</a>) by polling them locally over encrypted HTTP (<a href="https://en.wikipedia.org/wiki/JSON-RPC">JSON-RPC</a>). Whenever a device changes state, transitioning from idle to active (power consumption >  $0\, W$) or from active to idle (power consumption returning to $0\, W$), the service publishes an event to <a href="https://en.wikipedia.org/wiki/RabbitMQ">RabbitMQ</a>.</p></li>
<li><p align="justify"><b>Notification Service</b>: acts as a consumer of these events. It listens to the RabbitMQ queue, processes the incoming messages, and forwards notifications to end users. Currently, notifications are delivered via <a href="https://telegram.org/tour/channels">Telegram Channel</a> using the <a href="https://core.telegram.org/bots/api">Telegram Bot API</a>, but the system is extensible and can support additional channels (e.g., Signal, Discord, email) through dedicated adapters.</p></li>
</ol>

<p align="justify">RabbitMQ acts as the message broker and communication backbone between the microservices. It ensures that events are decoupled from their consumers, can be processed asynchronously, and remain reliable even if one service is temporarily unavailable. It’s worth noting that, messages are not persisted in the queue. If no subscriber is active at the time of publishing, the message will be lost. This is intentional as state-change events only carry value at the moment they occur. Once missed, the information becomes stale and no longer relevant.

This architecture allows SPN to:</a>
<ul>
<li><p align="justify">React in near real-time to device activity.</p></li>
<li><p align="justify">Scale horizontally by adding more consumers or producers.</p></li>
<li><p align="justify">Extend easily with new notification channels.</p></li>
</ul>

<p align="center">
<img
src="./resources/spn_diagram.svg?raw=true"
alt="SPN system diagram"
width="100%"
class="center"
/>
<p align="center">
    <label><b>Fig. 1</b>: SPN system instance overview</label>
    </p>
</p>

<p align="justify">The SPN was built out of a personal need for real-time notifications regarding cycles of my home washer and dryer machines, as shown in the diagram above. While I currently use only two smart plugs, the system was designed to support a large number of devices, making it scalable and flexible for broader home automation setups or small-scale deployments.</p>

## Setup

<p align="justify">SPN can be run easily using <a href="https://docs.docker.com/engine/containers/start-containers-automatically/">Docker</a> and <a href="https://docs.docker.com/compose/">Docker Compose</a>. Each service (<code>tapo_service</code> and <code>notification_service</code>) has its own Dockerfile. RabbitMQ is also run as a container.

### Prerequisites

<ul>
<li><p align="justify">A <code>.env</code> file with your environment variables (RabbitMQ credentials, Telegram bot token, Telegram channel ID).</p></li>
<li><p align="justify">A <code>settings.template.py</code> file with required configuration (e.g., device list). After editing, rename it to <code>settings.py</code> for each service.</p></li>
</ul>

<p align="justify">After cloning this repo start the SPN by running the following docker command:</p>

```bash
docker compose up -d --build
```
