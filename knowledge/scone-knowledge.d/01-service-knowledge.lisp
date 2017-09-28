(new-context {dharma} {general})
(in-context {dharma})

;; interfaces, service and method
(new-type {interface} {thing})
(new-type {service} {thing})
(new-type {method} {thing})
(new-type {argument} {thing})
(new-type {dharma-interface} {interface})
(new-type {dharma-service} {service})
(new-type {dharma-method} {method})
(new-type {dharma-argument} {argument})

(new-type-role {interface-method} {interface} {method})
(new-type-role {implemented-method} {dharma-interface} {dharma-method})
(new-type-role {required-argument} {dharma-method} {dharma-argument})
(new-type-role {returned-value} {dharma-method} {thing})
;; device
(new-type {device} {thing})
(new-type {dharma-device} {device})
(new-type-role {offered-service} {dharma-device} {dharma-service})
(new-type {proxy} {thing})
(new-type-role {service-proxy} {dharma-service} {proxy})




;; relations
(new-relation {performs action through}
	      :a-inst-of {dharma-service}
	      :b-inst-of {action}
	      :c-inst-of {dharma-method}
	      :transitive t)

(new-relation {causes event through}
	      :a-inst-of {dharma-service}
	      :b-inst-of {event}
	      :c-inst-of {dharma-method}
	      :transitive t)

(new-relation {is captured in}
	      :a-inst-of {thing}
	      :b-inst-of {thing})

(new-relation {is recognized in}
	      :a-inst-of {thing}
	      :b-inst-of {thing})

(new-relation {is detected in}
	      :a-inst-of {thing}
	      :b-inst-of {thing})

(new-relation {is found in}
	      :a-inst-of {thing}
	      :b-inst-of {thing})

;; concepts
(new-type-role {identity} {person} {thing})
(new-type-role {access credentials} {person} {thing})
(new-type {recognizer} {thing})
(new-type {snapshot} {thing})
(new-type {camera} {device})
(new-type {microphone} {device})
(new-type {finder} {thing})
(new-type {scene} {thing})
(new-type {sensor} {thing})
(new-type {motion} {thing})

(new-type {database} {file})
(new-type-role {image format} {image file} {thing})
(new-indv {jpg} {image format})
(new-indv {png} {image format})

(new-type-role {audio format} {audio file} {thing})
(new-indv {wav} {audio format})
(new-indv {mp3} {audio format})
(new-type {sound} {thing})
(new-type {command} {information object})

;; event types
(new-type {command execution by authorised person} {event})
(new-type {command recognition} {event})
(new-type {person recognition} {event})
(new-type {motion detected} {event})

