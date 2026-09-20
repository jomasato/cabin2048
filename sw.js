/* Cache-first, on purpose.
 *
 * This game's whole job is to work at 35,000 feet, so the network is never
 * allowed to sit between the player and the board - not even for a
 * revalidation that would stall for the length of an airline DNS timeout.
 * The cost is that a new build only lands when CACHE_VERSION changes below,
 * so bump it on every deploy. */
var CACHE_VERSION = "cabin2048-v3";

var ASSETS = [
  "./",
  "./index.html",
  "./manifest.webmanifest",
  "./icon-180.png",
  "./icon-192.png",
  "./icon-512.png",
  "./icon-maskable-512.png",
  "./favicon-32.png"
];

self.addEventListener("install", function(e){
  e.waitUntil(
    caches.open(CACHE_VERSION)
      .then(function(c){ return c.addAll(ASSETS); })
      .then(function(){ return self.skipWaiting(); })
  );
});

self.addEventListener("activate", function(e){
  e.waitUntil(
    caches.keys().then(function(keys){
      return Promise.all(keys.map(function(k){
        return k === CACHE_VERSION ? null : caches.delete(k);
      }));
    }).then(function(){ return self.clients.claim(); })
  );
});

self.addEventListener("fetch", function(e){
  var req = e.request;
  if (req.method !== "GET") return;

  /* Launching from the home screen is a navigation: answer it from the cache
     so a dead network never produces the offline dinosaur mid-flight. */
  if (req.mode === "navigate"){
    e.respondWith(
      caches.match("./index.html").then(function(hit){ return hit || fetch(req); })
    );
    return;
  }

  e.respondWith(
    caches.match(req).then(function(hit){ return hit || fetch(req); })
  );
});
