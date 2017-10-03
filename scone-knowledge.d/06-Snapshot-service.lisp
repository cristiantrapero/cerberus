(in-context {dharma})

(new-action-type {take_snapshot}
		 :agent-type {camera}
		 :object-type {scene}
		 :recipient-type {image file})

(new-action-type {record_video}
		 :agent-type {camera}
		 :object-type {scene}
		 :recipient-type {video file})

(new-context {take_snapshot bc} {dharma})
(new-is-a {take_snapshot bc} {before context})
(x-is-the-y-of-z {take_snapshot BC} {before context} {take_snapshot})
(new-context {take_snapshot ac} {take_snapshot bc})
(new-is-a {take_snapshot ac} {after context})
(x-is-the-y-of-z {take_snapshot ac} {after context} {take_snapshot})

(in-context {take_snapshot BC})
(new-not-statement (the-x-role-of-y {action object} {take_snapshot}) {is captured in}  (the-x-role-of-y {action recipient} {take_snapshot}))
(in-context {take_snapshot AC})
(new-statement (the-x-role-of-y {action object} {take_snapshot}) {is captured in}  (the-x-role-of-y {action recipient} {take_snapshot}))
(in-context {general})

(in-context {dharma})
(new-indv {SnapshotService-service-instance} {SnapshotService})
(new-indv {SnapshotService.setObserver} {dharma-method})
(new-is-a {SnapshotService.setObserver} {Observable.setObserver})
(new-indv {SnapshotService.trigger} {dharma-method})
(new-is-a {SnapshotService.trigger}  {DataSink.trigger})
(new-indv {SnapshotService.notify} {dharma-method})
(new-is-a {SnapshotService.notify} {EventSink.notify})
(x-is-a-y-of-z {SnapshotService.setObserver} {implemented-method} {SnapshotService-service-instance})
(x-is-a-y-of-z {SnapshotService.trigger} {implemented-method} {SnapshotService-service-instance})
(x-is-a-y-of-z {SnapshotService.notify} {implemented-method} {SnapshotService-service-instance})
(x-is-a-y-of-z {number} {required-argument} {SnapshotService.trigger})
(x-is-the-y-of-z {jpg} {returned-value} {SnapshotService.notify})


(new-statement {SnapshotService-service-instance}  {performs action through} {take_snapshot}
	       :c {SnapshotService.notify})

(new-type {scene snapshoted} {event})
(new-statement {take_snapshot} {causes} {scene snapshoted})
(new-statement {SnapshotService-service-instance} {causes event through} {scene snapshoted}
	       :c {DataSink.trigger})

;; Esto es temporal para testear el cliente
(new-indv {snapshot-service} {proxy})
(x-is-the-y-of-z {snapshot-service} {service-proxy} {SnapshotService-service-instance})
