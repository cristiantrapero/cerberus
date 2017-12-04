(in-context {dharma})

(new-action-type {capture_audio}
		 :agent-type {microphone}
		 :object-type {sound}
		 :recipient-type {audio file})


(new-context {capture_audio bc} {dharma})
(new-is-a {capture_audio bc} {before context})
(x-is-the-y-of-z {capture_audio BC} {before context} {capture_audio})

(new-context {capture_audio ac} {capture_audio bc})
(new-is-a {capture_audio ac} {after context})
(x-is-the-y-of-z {capture_audio ac} {after context} {capture_audio})

(in-context {capture_audio BC})
(new-indv {sound appears in the scene} {motion detected})

(in-context {capture_audio AC})
(new-indv {audio file recorded} {recorded audio})


(in-context {dharma})
(new-indv {ClipService-service-instance} {ClipService})
(new-indv {ClipService.setObserver} {dharma-method})
(new-is-a {ClipService.setObserver} {Observable.setObserver})
(new-indv {ClipService.notify} {dharma-method})
(new-is-a {ClipService.notify} {EventSink.notify})
(new-indv {ClipService.trigger} {dharma-method})
(new-is-a {ClipService.trigger}  {DataSink.trigger})
(x-is-a-y-of-z {ClipService.setObserver} {implemented-method} {ClipService-service-instance})
(x-is-a-y-of-z {ClipService.trigger} {implemented-method} {ClipService-service-instance})
(x-is-a-y-of-z {ClipService.notify} {implemented-method} {ClipService-service-instance})
(x-is-a-y-of-z {number} {required-argument} {ClipService.trigger})
(x-is-the-y-of-z {wav} {returned-value} {ClipService.notify})

(new-statement {ClipService-service-instance}  {performs action through} {capture_audio} :c {ClipService.notify})
(new-type {recorded audio} {event})

(new-statement {capture_audio} {causes} {recorded audio})
(new-statement {ClipService-service-instance} {causes event through} {recorded audio} :c {ClipService.trigger})


(new-indv {clip-service} {proxy})
(x-is-the-y-of-z {clip-service} {service-proxy} {ClipService-service-instance})
