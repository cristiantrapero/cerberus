;; Dharma semantic model
(new-context {dharma} {general})
(in-context {dharma})


;; Definition of interface, service, method and argument
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


;; Relations between device, service and proxy
(new-type {device} {thing})
(new-type {dharma-device} {device})
(new-type-role {offered-service} {dharma-device} {dharma-service})

(new-type {proxy} {thing})
(new-type-role {service-proxy} {dharma-service} {proxy})


;; Relations between entities
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
