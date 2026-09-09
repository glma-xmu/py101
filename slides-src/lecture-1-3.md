---
title: 'Lecture 1.3 · Project: A Web Crawler'
description: HTTP requests, file I/O, and streaming a download.
lang: en
source: resource/deck1_3_project.pptx
sections:
- id: project-overview
  title: Project overview
  start: 1
  level: 1
  textbook: ch1-4-iterators-0
  related: true
- id: downloading-an-image
  title: Downloading an image
  start: 3
  level: 1
  textbook: ch1-4-iterators-4
  related: true
- id: downloading-a-video
  title: Downloading a video
  start: 4
  level: 1
  textbook: ch1-4-iterators-4
  related: true
- id: streaming-in-chunks
  title: Streaming in chunks
  start: 6
  level: 1
  textbook: ch1-4-iterators-3
  related: true
---


<!-- slide: title-slide -->
<p class="eyebrow">Lecture 1.3</p>

# Project: A Web Crawler

## Python and Big Data in Economics

<p class="author">Guoliang Ma<br><span>The Chow Institute, 2026</span></p>

---

<!-- slide: lecture-import -->

## What you will learn

<div class="lecture-content" markdown="1">

<p class="">Putting the contents in Chapter 1 together to implement a web crawler:</p>
<p class="lecture-subpoint">installation of a package (module)</p>
<p class="lecture-subpoint">import a module</p>
<p class="lecture-subpoint">file I/O</p>
<p class="lecture-subpoint">dictionary</p>
<p class="lecture-subpoint">iterator</p>




</div>

---

<!-- slide: lecture-import -->

## A web crawler

<div class="lecture-content" markdown="1">

<p class=""><strong>Example 1.3.1</strong></p>
<p class="">import requests</p>
<p class=""><br>url = &quot;https://img1.baidu.com/it/u=2267280029,983346211&amp;fm=253&amp;fmt=auto&amp;app=120&amp;f=JPEG?w=500&amp;h=889&quot;</p>
<p class=""><br>r = requests.get(url=url)</p>
<p class=""><br>with open(&#x27;spongebob.png&#x27;, &#x27;wb&#x27;) as f:</p>
<p class="">f.write(r.content)</p>
<p class="caption">Disclaimer: The contents presented in this set of slides are only for educational purposes. You should NOT abuse the technique presented in the slides to unlawfully obtain any information from any websites.</p>




</div>

---

<!-- slide: lecture-import -->

## A web crawler

<div class="lecture-content" markdown="1">

<p class=""><strong>Example 1.3.2</strong></p>
<p class=""><code>import requests</code></p>
<p class=""><code>import time</code></p>
<p class=""><code>video_url = &quot;</code>https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/720/Big_Buck_Bunny_720_10s_1MB.mp4<code>&quot;</code></p>
<p class="caption">Disclaimer: The contents presented in this set of slides are only for educational purposes. You should NOT abuse the technique presented in the slides to unlawfully obtain any information from any websites.</p>




</div>

---

<!-- slide: lecture-import -->

## A web crawler

<div class="lecture-content" markdown="1">

<div class="columns" markdown="1">
<div class="column" markdown="1">
<p class=""><strong>Example 1.3.2 (Cont’d)</strong></p>
<p class="caption">Disclaimer: The contents presented in this set of slides are only for educational purposes. You should NOT abuse the technique presented in the slides to unlawfully obtain any information from any websites.</p>
</div>
<div class="column" markdown="1">

```python
stime = time.time()

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

r = requests.get(video_url, headers=header)

etime=time.time()
print(etime-stime)

with open("video.mp4", "wb") as f:
    f.write(r.content)
```


</div>
</div>

</div>

---

<!-- slide: lecture-import -->

## A web crawler

<div class="lecture-content" markdown="1">

<div class="columns" markdown="1">
<div class="column" markdown="1">
<p class=""><strong>Example 1.3.2 (Cont’d)</strong></p>
<p class="caption">Disclaimer: The contents presented in this set of slides are only for educational purposes. You should NOT abuse the technique presented in the slides to unlawfully obtain any information from any websites.</p>
</div>
<div class="column" markdown="1">

```python
r_iter = requests.get(video_url,
                      headers=header,
                      stream=True)

r_iter_len = int(r_iter.headers.get("Content-Length"))

print(r_iter_len)

with open('video_iter.mp4', 'wb') as f:
    write_all = 0
    for chunk in r_iter.iter_content(chunk_size=1024):
        write_all += f.write(chunk)
        print(f"{write_all / r_iter_len * 100}%")
```


</div>
</div>

</div>
