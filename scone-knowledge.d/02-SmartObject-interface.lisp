;; Data structures
(new-type {metadata} {information object})
(new-type {byteseq} {information object})
(new-is-a {image format} {information object})
(new-is-a {sound format} {information object})
(new-type {boolean} {information object})


;; Observable
(new-type {Observable} {dharma-interface})
(new-type {Observable.setObserver} {dharma-method})
(x-is-a-y-of-z {Observable.setObserver} {implemented-method} {Observable})


;; DataSink
(new-type {DataSink} {dharma-service})
(new-type {DataSink.notify} {dharma-method})
(x-is-a-y-of-z {DataSink.notify} {implemented-method} {DataSink})


;; EventSink
(new-type {EventSink} {dharma-interface})
(new-type {EventSink.notify} {dharma-method})
(x-is-a-y-of-z {EventSink.notify} {implemented-method} {EventSink})


;; DigitalSink
(new-type {DigitalSink} {dharma-interface})
(new-type {DigitalSink.notify} {dharma-method})
(x-is-a-y-of-z {DigitalSink.notify} {implemented-method} {DigitalSink})


;; SnapshotService
(new-type {SnapshotService} {dharma-service})
(new-is-a {SnapshotService} {Observable})
(new-is-a {SnapshotService} {EventSink})


;; ClipService
(new-type {ClipService} {dharma-service})
(new-is-a {ClipService} {Observable})
(new-is-a {ClipService} {EventSink})


;; PersonRecognizer
(new-type {PersonRecognizer} {dharma-service})
(new-is-a {PersonRecognizer} {DataSink})
(new-is-a {PersonRecognizer} {Observable})


;; SpeechToText
(new-type {SpeechToText} {dharma-service})
(new-is-a {SpeechToText} {DataSink})
(new-is-a {SpeechToText} {Observable})


;; AuthenticatedCommandService
(new-type {AuthenticatedCommandService} {dharma-service})
(new-is-a {AuthenticatedCommandService} {Observable})
(new-type {AuthenticatedCommandService.notifyPerson} {dharma-method})
(new-type {AuthenticatedCommandService.notifyCommand} {dharma-method})
(x-is-a-y-of-z {AuthenticatedCommandService.notifyPerson} {implemented-method} {AuthenticatedCommandService})
(x-is-a-y-of-z {AuthenticatedCommandService.notifyCommand} {implemented-method} {AuthenticatedCommandService})
