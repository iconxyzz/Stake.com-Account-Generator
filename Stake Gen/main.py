import tls_client
import threading
import concurrent.futures
import time
import string
import random
import subprocess
import ctypes,json,os;os.system("cls")
from colorama import Fore,Style;blue = Fore.BLUE;red = Fore.RED;warn = Fore.YELLOW;green = Fore.GREEN;gray = Fore.LIGHTBLACK_EX;white_red = Fore.LIGHTRED_EX;white_green = Fore.LIGHTGREEN_EX;white_warn = Fore.LIGHTYELLOW_EX;white_blue = Fore.LIGHTBLUE_EX
from datetime import datetime
import tls_client,requests as rr;ss=rr.Session()
from user_agents import parse
import re,ctypes
from base64 import b64encode as encoder, b64decode as decoder
UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

generated = 0
timeouted = 0
failed = 0
title = "Stake.com Token Generator |     [Generated: {} /      Failed : {} /      Timeouted : {}]     |       enjoy."
settings = json.loads(open("settings.json").read())
THREADS = settings["threads"]
capApiKey = settings["captcha_key"]
captchaService = settings["captcha_service"]
confirmVerification = settings["confirmMailVerification"]
proxyType = settings["proxyType"]
proxies = open("proxies.txt").read().splitlines()
ctypes.windll.kernel32.SetConsoleTitleW("Stake.com Token Generator |     [Generated: 0 /      Failed : 0 /      Timeouted : 0]     |       enjoy.")
def setup_console():
    os.system("mode con: cols=220 lines=50")
    console_handle = ctypes.windll.kernel32.GetConsoleWindow()
    screen_width, screen_height = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)
    x, y = screen_width//25, screen_height//20
    ctypes.windll.user32.SetWindowPos(console_handle, 0, x, y, 0, 0, 0x0001)

setup_console()
class Console:
    def __init__(self,debug=False) -> None:
        self.debug = debug
    def error(self,x):
        x = str(x)
        if self.debug:
            print(f"{red}[- ERROR -]{Style.RESET_ALL} - {gray}[{datetime.now().date()} - {datetime.now().now().strftime('%H:%M:%S')}]{Style.RESET_ALL} |\t {white_red+x}{Style.RESET_ALL}")
        else:
            print(f"{red}[-]{Style.RESET_ALL}\t {red+x}{Style.RESET_ALL}")
    def success(self,x):
        x = str(x)
        if self.debug:
            print(f"{green}[+ Success +]{Style.RESET_ALL} - {gray}[{datetime.now().date()} - {datetime.now().now().strftime('%H:%M:%S')}]{Style.RESET_ALL} |\t {white_green+x}{Style.RESET_ALL}")
        else:
            print(f"{green}[+]{Style.RESET_ALL}\t {white_green+x}{Style.RESET_ALL}")
    def warn(self,x,t=0):
        x = str(x)
        if self.debug:
            print(f"{warn}[! {'WARNING' if t == 0 else 'FAILED'} !]{Style.RESET_ALL} - {gray}[{datetime.now().date()} - {datetime.now().now().strftime('%H:%M:%S')}]{Style.RESET_ALL} |\t {white_warn+x}{Style.RESET_ALL}")
        else:
            print(f"{warn}[!]{Style.RESET_ALL}\t {white_warn+x}{Style.RESET_ALL}")

console = Console(debug=True)

class BypassCloudflare:
    def __init__(self, requests, proxy=None, cookies:dict=None, useragent: str=UserAgent):
        self.client = requests
        self.useragent = useragent
        self.proxy = proxy
        self.cookies = cookies
        self.r = self.client.get("https://stake.com/?tab=register&modal=auth", proxy=proxy, cookies=cookies).text.split("r:'",1)[1].split("'",2)[0]
        self.s, self.key = self._get_values()
        self.base_data = {
            '0': ['length', 'innerWidth', 'innerHeight', 'scrollX', 'pageXOffset', 'scrollY', 'pageYOffset', 'screenX', 'screenY', 'screenLeft', 'screenTop', 'TEMPORARY', 'n.maxTouchPoints'],
            '1': ['PERSISTENT', 'd.childElementCount', 'd.ELEMENT_NODE', 'd.DOCUMENT_POSITION_DISCONNECTED'],
            '2': ['d.ATTRIBUTE_NODE', 'd.DOCUMENT_POSITION_PRECEDING'],
            '3': ['d.TEXT_NODE'],
            '4': ['d.CDATA_SECTION_NODE', 'd.DOCUMENT_POSITION_FOLLOWING'],
            '5': ['d.ENTITY_REFERENCE_NODE'],
            '6': ['d.ENTITY_NODE'],
            '7': ['d.PROCESSING_INSTRUCTION_NODE'],
            '8': ['n.deviceMemory', 'd.COMMENT_NODE', 'd.DOCUMENT_POSITION_CONTAINS'],
            '9': ['d.nodeType', 'd.DOCUMENT_NODE'],
            '10': ['d.DOCUMENT_TYPE_NODE'],
            '11': ['d.DOCUMENT_FRAGMENT_NODE'],
            '12': ['n.hardwareConcurrency', 'd.NOTATION_NODE'],
            '16': ['d.DOCUMENT_POSITION_CONTAINED_BY'],
            '32': ['d.DOCUMENT_POSITION_IMPLEMENTATION_SPECIFIC'],
            '1032': ['outerHeight'],
            '1920': ['outerWidth'],
            'o': ['window', 'self', 'document', 'location', 'customElements', 'history', 'navigation', 'locationbar', 'menubar',
                  'personalbar', 'scrollbars', 'statusbar', 'toolbar', 'frames', 'top', 'parent', 'frameElement', 'navigator',
                  'external', 'screen', 'visualViewport', 'clientInformation', 'styleMedia', 'trustedTypes', 'performance',
                  'crypto', 'indexedDB', 'sessionStorage', 'localStorage', 'scheduler', 'chrome', 'caches', 'cookieStore',
                  'launchQueue', 'speechSynthesis', 'globalThis', 'JSON', 'Math', 'Intl', 'Atomics', 'Reflect', 'console',
                  'CSS', 'WebAssembly', 'GPUBufferUsage', 'GPUColorWrite', 'GPUMapMode', 'GPUShaderStage', 'GPUTextureUsage',
                  'n.scheduling', 'n.userActivation', 'n.geolocation', 'n.connection', 'n.plugins', 'n.mimeTypes',
                  'n.webkitTemporaryStorage', 'n.webkitPersistentStorage', 'n.bluetooth', 'n.clipboard', 'n.credentials',
                  'n.keyboard', 'n.managed', 'n.mediaDevices', 'n.storage', 'n.serviceWorker', 'n.virtualKeyboard',
                  'n.wakeLock', 'n.ink', 'n.hid', 'n.locks', 'n.mediaCapabilities', 'n.mediaSession', 'n.permissions',
                  'n.presentation', 'n.serial', 'n.gpu', 'n.usb', 'n.windowControlsOverlay', 'n.xr', 'n.userAgentData',
                  'd.location', 'd.implementation', 'd.documentElement', 'd.body', 'd.head', 'd.images', 'd.embeds',
                  'd.plugins', 'd.links', 'd.forms', 'd.scripts', 'd.defaultView', 'd.anchors', 'd.applets',
                  'd.scrollingElement', 'd.featurePolicy', 'd.children', 'd.firstElementChild', 'd.lastElementChild',
                  'd.activeElement', 'd.styleSheets', 'd.fonts', 'd.fragmentDirective', 'd.timeline', 'd.childNodes',
                  'd.firstChild', 'd.lastChild'],
            'false': ['closed', 'crossOriginIsolated', 'credentialless', 'originAgentCluster', 'n.webdriver', 'd.xmlStandalone', 'd.hidden', 'd.wasDiscarded', 'd.prerendering', 'd.webkitHidden', 'd.fullscreen', 'd.webkitIsFullScreen'],
            'x': ['opener', 'onsearch', 'onappinstalled', 'onbeforeinstallprompt', 'onbeforexrselect', 'onabort',
                  'onbeforeinput', 'onblur', 'oncancel', 'oncanplay', 'oncanplaythrough', 'onchange', 'onclick', 'onclose',
                  'oncontextlost', 'oncontextmenu', 'oncontextrestored', 'oncuechange', 'ondblclick', 'ondrag', 'ondragend',
                  'ondragenter', 'ondragleave', 'ondragover', 'ondragstart', 'ondrop', 'ondurationchange', 'onemptied',
                  'onended', 'onerror', 'onfocus', 'onformdata', 'oninput', 'oninvalid', 'onkeydown', 'onkeypress', 'onkeyup',
                  'onload', 'onloadeddata', 'onloadedmetadata', 'onloadstart', 'onmousedown', 'onmouseenter', 'onmouseleave',
                  'onmousemove', 'onmouseout', 'onmouseover', 'onmouseup', 'onmousewheel', 'onpause', 'onplay', 'onplaying',
                  'onprogress', 'onratechange', 'onreset', 'onresize', 'onscroll', 'onsecuritypolicyviolation', 'onseeked',
                  'onseeking', 'onselect', 'onslotchange', 'onstalled', 'onsubmit', 'onsuspend', 'ontimeupdate', 'ontoggle',
                  'onvolumechange', 'onwaiting', 'onwebkitanimationend', 'onwebkitanimationiteration','onwebkitanimationstart',
                  'onwebkittransitionend', 'onwheel', 'onauxclick', 'ongotpointercapture', 'onlostpointercapture',
                  'onpointerdown', 'onpointermove', 'onpointerrawupdate', 'onpointerup', 'onpointercancel', 'onpointerover',
                  'onpointerout', 'onpointerenter', 'onpointerleave', 'onselectstart', 'onselectionchange', 'onanimationend',
                  'onanimationiteration', 'onanimationstart', 'ontransitionrun', 'ontransitionstart', 'ontransitionend',
                  'ontransitioncancel', 'onafterprint', 'onbeforeprint', 'onbeforeunload', 'onhashchange', 'onlanguagechange',
                  'onmessage', 'onmessageerror', 'onoffline', 'ononline', 'onpagehide', 'onpageshow', 'onpopstate',
                  'onrejectionhandled', 'onstorage', 'onunhandledrejection', 'onunload', 'ondevicemotion',
                  'ondeviceorientation', 'ondeviceorientationabsolute', 'onbeforematch', 'onbeforetoggle',
                  'oncontentvisibilityautostatechange', 'onscrollend', 'n.doNotTrack', 'd.doctype', 'd.xmlEncoding',
                  'd.xmlVersion', 'd.currentScript', 'd.onreadystatechange', 'd.all', 'd.onpointerlockchange',
                  'd.onpointerlockerror', 'd.onbeforecopy', 'd.onbeforecut', 'd.onbeforepaste', 'd.onfreeze',
                  'd.onprerenderingchange', 'd.onresume', 'd.onsearch', 'd.onvisibilitychange', 'd.onfullscreenchange',
                  'd.onfullscreenerror', 'd.webkitCurrentFullScreenElement', 'd.webkitFullscreenElement',
                  'd.onwebkitfullscreenchange', 'd.onwebkitfullscreenerror', 'd.rootElement',  'd.pictureInPictureElement',
                  'd.onbeforexrselect', 'd.onabort', 'd.onbeforeinput', 'd.onblur', 'd.oncancel', 'd.oncanplay',
                  'd.oncanplaythrough', 'd.onchange', 'd.onclick', 'd.onclose', 'd.oncontextlost', 'd.oncontextmenu',
                  'd.oncontextrestored', 'd.oncuechange', 'd.ondblclick', 'd.ondrag', 'd.ondragend', 'd.ondragenter',
                  'd.ondragleave', 'd.ondragover', 'd.ondragstart', 'd.ondrop', 'd.ondurationchange', 'd.onemptied',
                  'd.onended', 'd.onerror', 'd.onfocus', 'd.onformdata', 'd.oninput', 'd.oninvalid', 'd.onkeydown',
                  'd.onkeypress', 'd.onkeyup', 'd.onload', 'd.onloadeddata', 'd.onloadedmetadata', 'd.onloadstart',
                  'd.onmousedown', 'd.onmouseenter', 'd.onmouseleave', 'd.onmousemove', 'd.onmouseout', 'd.onmouseover',
                  'd.onmouseup', 'd.onmousewheel', 'd.onpause', 'd.onplay', 'd.onplaying', 'd.onprogress','d.onratechange',
                  'd.onreset', 'd.onresize', 'd.onscroll', 'd.onsecuritypolicyviolation', 'd.onseeked', 'd.onseeking',
                  'd.onselect', 'd.onslotchange', 'd.onstalled', 'd.onsubmit', 'd.onsuspend', 'd.ontimeupdate', 'd.ontoggle',
                  'd.onvolumechange', 'd.onwaiting', 'd.onwebkitanimationend', 'd.onwebkitanimationiteration',
                  'd.onwebkitanimationstart', 'd.onwebkittransitionend', 'd.onwheel', 'd.onauxclick', 'd.ongotpointercapture',
                  'd.onlostpointercapture', 'd.onpointerdown', 'd.onpointermove', 'd.onpointerrawupdate', 'd.onpointerup',
                  'd.onpointercancel', 'd.onpointerover', 'd.onpointerout', 'd.onpointerenter', 'd.onpointerleave',
                  'd.onselectstart', 'd.onselectionchange', 'd.onanimationend', 'd.onanimationiteration', 'd.onanimationstart',
                  'd.ontransitionrun', 'd.ontransitionstart', 'd.ontransitionend', 'd.ontransitioncancel', 'd.oncopy',
                  'd.oncut', 'd.onpaste', 'd.pointerLockElement', 'd.fullscreenElement', 'd.onbeforematch', 'd.onbeforetoggle',
                  'd.oncontentvisibilityautostatechange', 'd.onscrollend', 'd.ownerDocument', 'd.parentNode', 'd.parentElement',
                  'd.previousSibling', 'd.nextSibling', 'd.nodeValue', 'd.textContent'], 'https://stake.com': ['origin'],
            '0.8999999761581421': ['devicePixelRatio'],
            'true': ['isSecureContext', 'offscreenBuffering', 'n.pdfViewerEnabled', 'n.cookieEnabled', 'n.onLine', 'd.fullscreenEnabled', 'd.webkitFullscreenEnabled', 'd.pictureInPictureEnabled', 'd.isConnected'],
            'N': ['alert', 'atob', 'blur', 'btoa', 'cancelAnimationFrame', 'cancelIdleCallback', 'captureEvents',
                  'clearInterval', 'clearTimeout', 'close', 'confirm', 'createImageBitmap', 'fetch', 'find', 'focus',
                  'getComputedStyle', 'getSelection', 'matchMedia', 'moveBy', 'moveTo', 'open', 'postMessage', 'print',
                  'prompt', 'queueMicrotask', 'releaseEvents', 'reportError', 'requestAnimationFrame', 'requestIdleCallback',
                  'resizeBy', 'resizeTo', 'scroll', 'scrollBy', 'scrollTo', 'setInterval', 'setTimeout', 'stop',
                  'structuredClone', 'webkitCancelAnimationFrame', 'webkitRequestAnimationFrame', 'getScreenDetails',
                  'queryLocalFonts', 'showDirectoryPicker', 'showOpenFilePicker', 'showSaveFilePicker', 'openDatabase',
                  'webkitRequestFileSystem', 'webkitResolveLocalFileSystemURL', 'addEventListener', 'dispatchEvent',
                  'removeEventListener', 'Object', 'Function', 'Number', 'parseFloat', 'parseInt', 'Boolean', 'String',
                  'Symbol', 'Date', 'Promise', 'RegExp', 'Error', 'AggregateError', 'EvalError', 'RangeError', 'ReferenceError',
                  'SyntaxError', 'TypeError', 'URIError', 'ArrayBuffer', 'Uint8Array', 'Int8Array', 'Uint16Array', 'Int16Array',
                  'Uint32Array', 'Int32Array', 'Float32Array', 'Float64Array', 'Uint8ClampedArray', 'BigUint64Array',
                  'BigInt64Array', 'DataView', 'Map', 'BigInt', 'Set', 'WeakMap', 'WeakSet', 'Proxy', 'FinalizationRegistry',
                  'WeakRef', 'decodeURI', 'decodeURIComponent', 'encodeURI', 'encodeURIComponent', 'escape', 'unescape', 'eval',
                  'isFinite', 'isNaN', 'Option', 'Image', 'Audio', 'webkitURL', 'webkitRTCPeerConnection', 'webkitMediaStream',
                  'WebKitMutationObserver', 'WebKitCSSMatrix', 'XSLTProcessor', 'XPathResult', 'XPathExpression',
                  'XPathEvaluator', 'XMLSerializer', 'XMLHttpRequestUpload', 'XMLHttpRequestEventTarget', 'XMLHttpRequest',
                  'XMLDocument', 'WritableStreamDefaultWriter', 'WritableStreamDefaultController', 'WritableStream', 'Worker',
                  'Window', 'WheelEvent', 'WebSocket', 'WebGLVertexArrayObject', 'WebGLUniformLocation',
                  'WebGLTransformFeedback', 'WebGLTexture', 'WebGLSync', 'WebGLShaderPrecisionFormat', 'WebGLShader',
                  'WebGLSampler', 'WebGLRenderingContext', 'WebGLRenderbuffer', 'WebGLQuery', 'WebGLProgram',
                  'WebGLFramebuffer', 'WebGLContextEvent', 'WebGLBuffer', 'WebGLActiveInfo', 'WebGL2RenderingContext',
                  'WaveShaperNode', 'VisualViewport', 'VirtualKeyboardGeometryChangeEvent', 'ValidityState', 'VTTCue',
                  'UserActivation', 'URLSearchParams', 'URLPattern', 'URL', 'UIEvent', 'TrustedTypePolicyFactory',
                  'TrustedTypePolicy', 'TrustedScriptURL', 'TrustedScript', 'TrustedHTML', 'TreeWalker', 'TransitionEvent',
                  'TransformStreamDefaultController', 'TransformStream', 'TrackEvent', 'TouchList', 'TouchEvent', 'Touch',
                  'TimeRanges', 'TextTrackList', 'TextTrackCueList', 'TextTrackCue', 'TextTrack', 'TextMetrics', 'TextEvent',
                  'TextEncoderStream', 'TextEncoder', 'TextDecoderStream', 'TextDecoder', 'Text', 'TaskSignal',
                  'TaskPriorityChangeEvent', 'TaskController', 'TaskAttributionTiming', 'SyncManager', 'SubmitEvent',
                  'StyleSheetList', 'StyleSheet', 'StylePropertyMapReadOnly', 'StylePropertyMap', 'StorageEvent', 'Storage',
                  'StereoPannerNode', 'StaticRange', 'SourceBufferList', 'SourceBuffer', 'ShadowRoot', 'Selection',
                  'SecurityPolicyViolationEvent', 'ScriptProcessorNode', 'ScreenOrientation', 'Screen', 'Scheduling',
                  'Scheduler', 'SVGViewElement', 'SVGUseElement', 'SVGUnitTypes', 'SVGTransformList', 'SVGTransform',
                  'SVGTitleElement', 'SVGTextPositioningElement', 'SVGTextPathElement', 'SVGTextElement',
                  'SVGTextContentElement', 'SVGTSpanElement', 'SVGSymbolElement', 'SVGSwitchElement', 'SVGStyleElement',
                  'SVGStringList', 'SVGStopElement', 'SVGSetElement', 'SVGScriptElement', 'SVGSVGElement', 'SVGRectElement',
                  'SVGRect', 'SVGRadialGradientElement', 'SVGPreserveAspectRatio', 'SVGPolylineElement', 'SVGPolygonElement',
                  'SVGPointList', 'SVGPoint', 'SVGPatternElement', 'SVGPathElement', 'SVGNumberList', 'SVGNumber',
                  'SVGMetadataElement', 'SVGMatrix', 'SVGMaskElement', 'SVGMarkerElement', 'SVGMPathElement',
                  'SVGLinearGradientElement', 'SVGLineElement', 'SVGLengthList', 'SVGLength', 'SVGImageElement',
                  'SVGGraphicsElement', 'SVGGradientElement', 'SVGGeometryElement', 'SVGGElement', 'SVGForeignObjectElement',
                  'SVGFilterElement', 'SVGFETurbulenceElement', 'SVGFETileElement', 'SVGFESpotLightElement',
                  'SVGFESpecularLightingElement', 'SVGFEPointLightElement', 'SVGFEOffsetElement', 'SVGFEMorphologyElement',
                  'SVGFEMergeNodeElement', 'SVGFEMergeElement', 'SVGFEImageElement', 'SVGFEGaussianBlurElement',
                  'SVGFEFuncRElement', 'SVGFEFuncGElement', 'SVGFEFuncBElement', 'SVGFEFuncAElement', 'SVGFEFloodElement',
                  'SVGFEDropShadowElement', 'SVGFEDistantLightElement', 'SVGFEDisplacementMapElement',
                  'SVGFEDiffuseLightingElement', 'SVGFEConvolveMatrixElement', 'SVGFECompositeElement',
                  'SVGFEComponentTransferElement', 'SVGFEColorMatrixElement', 'SVGFEBlendElement', 'SVGEllipseElement',
                  'SVGElement', 'SVGDescElement', 'SVGDefsElement', 'SVGComponentTransferFunctionElement', 'SVGClipPathElement',
                  'SVGCircleElement', 'SVGAnimationElement', 'SVGAnimatedTransformList', 'SVGAnimatedString', 'SVGAnimatedRect',
                  'SVGAnimatedPreserveAspectRatio', 'SVGAnimatedNumberList', 'SVGAnimatedNumber', 'SVGAnimatedLengthList',
                  'SVGAnimatedLength', 'SVGAnimatedInteger', 'SVGAnimatedEnumeration', 'SVGAnimatedBoolean', 'SVGAnimatedAngle',
                  'SVGAnimateTransformElement', 'SVGAnimateMotionElement', 'SVGAnimateElement', 'SVGAngle', 'SVGAElement',
                  'Response', 'ResizeObserverSize', 'ResizeObserverEntry', 'ResizeObserver', 'Request', 'ReportingObserver',
                  'ReadableStreamDefaultReader', 'ReadableStreamDefaultController', 'ReadableStreamBYOBRequest',
                  'ReadableStreamBYOBReader', 'ReadableStream', 'ReadableByteStreamController', 'Range', 'RadioNodeList',
                  'RTCTrackEvent', 'RTCStatsReport', 'RTCSessionDescription', 'RTCSctpTransport', 'RTCRtpTransceiver',
                  'RTCRtpSender', 'RTCRtpReceiver', 'RTCPeerConnectionIceEvent', 'RTCPeerConnectionIceErrorEvent',
                  'RTCPeerConnection', 'RTCIceTransport', 'RTCIceCandidate', 'RTCErrorEvent', 'RTCError',
                  'RTCEncodedVideoFrame', 'RTCEncodedAudioFrame', 'RTCDtlsTransport', 'RTCDataChannelEvent', 'RTCDataChannel',
                  'RTCDTMFToneChangeEvent', 'RTCDTMFSender', 'RTCCertificate', 'PromiseRejectionEvent', 'ProgressEvent',
                  'Profiler', 'ProcessingInstruction', 'PopStateEvent', 'PointerEvent', 'PluginArray', 'Plugin',
                  'PictureInPictureWindow', 'PictureInPictureEvent', 'PeriodicWave', 'PerformanceTiming',
                  'PerformanceServerTiming', 'PerformanceResourceTiming', 'PerformancePaintTiming',
                  'PerformanceObserverEntryList', 'PerformanceObserver', 'PerformanceNavigationTiming','PerformanceNavigation',
                  'PerformanceMeasure', 'PerformanceMark', 'PerformanceLongTaskTiming', 'PerformanceEventTiming',
                  'PerformanceEntry', 'PerformanceElementTiming', 'Performance', 'Path2D', 'PannerNode', 'PageTransitionEvent',
                  'OverconstrainedError', 'OscillatorNode', 'OffscreenCanvasRenderingContext2D', 'OffscreenCanvas',
                  'OfflineAudioContext', 'OfflineAudioCompletionEvent', 'NodeList', 'NodeIterator', 'NodeFilter', 'Node',
                  'NetworkInformation', 'Navigator', 'NavigationTransition', 'NavigationHistoryEntry', 'NavigationDestination',
                  'NavigationCurrentEntryChangeEvent', 'Navigation', 'NavigateEvent', 'NamedNodeMap', 'MutationRecord',
                  'MutationObserver', 'MutationEvent', 'MouseEvent', 'MimeTypeArray', 'MimeType', 'MessagePort', 'MessageEvent',
                  'MessageChannel', 'MediaStreamTrackProcessor', 'MediaStreamTrackGenerator', 'MediaStreamTrackEvent',
                  'MediaStreamTrack', 'MediaStreamEvent', 'MediaStreamAudioSourceNode', 'MediaStreamAudioDestinationNode',
                  'MediaStream', 'MediaSourceHandle', 'MediaSource', 'MediaRecorder', 'MediaQueryListEvent', 'MediaQueryList',
                  'MediaList', 'MediaError', 'MediaEncryptedEvent', 'MediaElementAudioSourceNode', 'MediaCapabilities',
                  'Location', 'LayoutShiftAttribution', 'LayoutShift', 'LargestContentfulPaint', 'KeyframeEffect',
                  'KeyboardEvent', 'IntersectionObserverEntry', 'IntersectionObserver', 'InputEvent', 'InputDeviceInfo',
                  'InputDeviceCapabilities', 'ImageData', 'ImageCapture', 'ImageBitmapRenderingContext', 'ImageBitmap',
                  'IdleDeadline', 'IIRFilterNode', 'IDBVersionChangeEvent', 'IDBTransaction', 'IDBRequest', 'IDBOpenDBRequest',
                  'IDBObjectStore', 'IDBKeyRange', 'IDBIndex', 'IDBFactory', 'IDBDatabase', 'IDBCursorWithValue', 'IDBCursor',
                  'History', 'Headers', 'HashChangeEvent', 'HTMLVideoElement', 'HTMLUnknownElement', 'HTMLUListElement',
                  'HTMLTrackElement', 'HTMLTitleElement', 'HTMLTimeElement', 'HTMLTextAreaElement', 'HTMLTemplateElement',
                  'HTMLTableSectionElement', 'HTMLTableRowElement', 'HTMLTableElement', 'HTMLTableColElement',
                  'HTMLTableCellElement', 'HTMLTableCaptionElement', 'HTMLStyleElement', 'HTMLSpanElement', 'HTMLSourceElement',
                  'HTMLSlotElement', 'HTMLSelectElement', 'HTMLScriptElement', 'HTMLQuoteElement', 'HTMLProgressElement',
                  'HTMLPreElement', 'HTMLPictureElement', 'HTMLParamElement', 'HTMLParagraphElement', 'HTMLOutputElement',
                  'HTMLOptionsCollection', 'HTMLOptionElement', 'HTMLOptGroupElement', 'HTMLObjectElement', 'HTMLOListElement',
                  'HTMLModElement', 'HTMLMeterElement', 'HTMLMetaElement', 'HTMLMenuElement', 'HTMLMediaElement',
                  'HTMLMarqueeElement', 'HTMLMapElement', 'HTMLLinkElement', 'HTMLLegendElement', 'HTMLLabelElement',
                  'HTMLLIElement', 'HTMLInputElement', 'HTMLImageElement', 'HTMLIFrameElement', 'HTMLHtmlElement',
                  'HTMLHeadingElement', 'HTMLHeadElement', 'HTMLHRElement', 'HTMLFrameSetElement', 'HTMLFrameElement',
                  'HTMLFormElement', 'HTMLFormControlsCollection', 'HTMLFontElement', 'HTMLFieldSetElement', 'HTMLEmbedElement',
                  'HTMLElement', 'HTMLDocument', 'HTMLDivElement', 'HTMLDirectoryElement', 'HTMLDialogElement',
                  'HTMLDetailsElement', 'HTMLDataListElement', 'HTMLDataElement', 'HTMLDListElement', 'HTMLCollection',
                  'HTMLCanvasElement', 'HTMLButtonElement', 'HTMLBodyElement', 'HTMLBaseElement', 'HTMLBRElement',
                  'HTMLAudioElement', 'HTMLAreaElement', 'HTMLAnchorElement', 'HTMLAllCollection', 'GeolocationPositionError',
                  'GeolocationPosition', 'GeolocationCoordinates', 'Geolocation', 'GamepadHapticActuator', 'GamepadEvent',
                  'GamepadButton', 'Gamepad', 'GainNode', 'FormDataEvent', 'FormData', 'FontFaceSetLoadEvent', 'FontFace',
                  'FocusEvent', 'FileReader', 'FileList', 'File', 'FeaturePolicy', 'External', 'EventTarget', 'EventSource',
                  'EventCounts', 'Event', 'ErrorEvent', 'ElementInternals', 'Element', 'DynamicsCompressorNode', 'DragEvent',
                  'DocumentType', 'DocumentFragment', 'Document', 'DelayNode', 'DecompressionStream', 'DataTransferItemList',
                  'DataTransferItem', 'DataTransfer', 'DOMTokenList', 'DOMStringMap', 'DOMStringList', 'DOMRectReadOnly',
                  'DOMRectList', 'DOMRect', 'DOMQuad', 'DOMPointReadOnly', 'DOMPoint', 'DOMParser', 'DOMMatrixReadOnly',
                  'DOMMatrix', 'DOMImplementation', 'DOMException', 'DOMError', 'CustomStateSet', 'CustomEvent',
                  'CustomElementRegistry', 'Crypto', 'CountQueuingStrategy', 'ConvolverNode', 'ConstantSourceNode',
                  'CompressionStream', 'CompositionEvent', 'Comment', 'CloseEvent', 'ClipboardEvent', 'CharacterData',
                  'ChannelSplitterNode', 'ChannelMergerNode', 'CanvasRenderingContext2D', 'CanvasPattern', 'CanvasGradient',
                  'CanvasCaptureMediaStreamTrack', 'CSSVariableReferenceValue', 'CSSUnparsedValue', 'CSSUnitValue',
                  'CSSTranslate', 'CSSTransformValue', 'CSSTransformComponent', 'CSSSupportsRule', 'CSSStyleValue',
                  'CSSStyleSheet', 'CSSStyleRule', 'CSSStyleDeclaration', 'CSSSkewY', 'CSSSkewX', 'CSSSkew', 'CSSScale',
                  'CSSRuleList', 'CSSRule', 'CSSRotate', 'CSSPropertyRule', 'CSSPositionValue', 'CSSPerspective', 'CSSPageRule',
                  'CSSNumericValue', 'CSSNumericArray', 'CSSNamespaceRule', 'CSSMediaRule', 'CSSMatrixComponent',
                  'CSSMathValue', 'CSSMathSum', 'CSSMathProduct', 'CSSMathNegate', 'CSSMathMin', 'CSSMathMax', 'CSSMathInvert',
                  'CSSMathClamp', 'CSSLayerStatementRule', 'CSSLayerBlockRule', 'CSSKeywordValue', 'CSSKeyframesRule',
                  'CSSKeyframeRule', 'CSSImportRule', 'CSSImageValue', 'CSSGroupingRule', 'CSSFontPaletteValuesRule',
                  'CSSFontFaceRule', 'CSSCounterStyleRule', 'CSSContainerRule', 'CSSConditionRule', 'CDATASection',
                  'ByteLengthQueuingStrategy', 'BroadcastChannel', 'BlobEvent', 'Blob', 'BiquadFilterNode', 'BeforeUnloadEvent',
                  'BeforeInstallPromptEvent', 'BaseAudioContext', 'BarProp', 'AudioWorkletNode', 'AudioSinkInfo',
                  'AudioScheduledSourceNode', 'AudioProcessingEvent', 'AudioParamMap', 'AudioParam', 'AudioNode',
                  'AudioListener', 'AudioDestinationNode', 'AudioContext', 'AudioBufferSourceNode', 'AudioBuffer', 'Attr',
                  'AnimationEvent', 'AnimationEffect', 'Animation', 'AnalyserNode', 'AbstractRange', 'AbortSignal',
                  'AbortController', 'AbsoluteOrientationSensor', 'Accelerometer', 'AudioWorklet', 'BatteryManager', 'Cache',
                  'CacheStorage', 'Clipboard', 'ClipboardItem', 'CookieChangeEvent', 'CookieStore', 'CookieStoreManager',
                  'Credential', 'CredentialsContainer', 'CryptoKey', 'DeviceMotionEvent', 'DeviceMotionEventAcceleration',
                  'DeviceMotionEventRotationRate', 'DeviceOrientationEvent', 'FederatedCredential', 'GravitySensor',
                  'Gyroscope', 'Keyboard', 'KeyboardLayoutMap', 'LinearAccelerationSensor', 'Lock', 'LockManager', 'MIDIAccess',
                  'MIDIConnectionEvent', 'MIDIInput', 'MIDIInputMap', 'MIDIMessageEvent', 'MIDIOutput', 'MIDIOutputMap',
                  'MIDIPort', 'MediaDeviceInfo', 'MediaDevices', 'MediaKeyMessageEvent', 'MediaKeySession', 'MediaKeyStatusMap',
                  'MediaKeySystemAccess', 'MediaKeys', 'NavigationPreloadManager', 'NavigatorManagedData', 'OrientationSensor',
                  'PasswordCredential', 'RelativeOrientationSensor', 'Sanitizer', 'ScreenDetailed', 'ScreenDetails', 'Sensor',
                  'SensorErrorEvent', 'ServiceWorker', 'ServiceWorkerContainer', 'ServiceWorkerRegistration', 'StorageManager',
                  'SubtleCrypto', 'VirtualKeyboard', 'WebTransport', 'WebTransportBidirectionalStream',
                  'WebTransportDatagramDuplexStream', 'WebTransportError', 'Worklet', 'XRDOMOverlayState', 'XRLayer',
                  'XRWebGLBinding', 'AudioData', 'EncodedAudioChunk', 'EncodedVideoChunk', 'ImageTrack', 'ImageTrackList',
                  'VideoColorSpace', 'VideoFrame', 'AudioDecoder', 'AudioEncoder', 'ImageDecoder', 'VideoDecoder',
                  'VideoEncoder', 'AuthenticatorAssertionResponse', 'AuthenticatorAttestationResponse', 'AuthenticatorResponse',
                  'PublicKeyCredential', 'Bluetooth', 'BluetoothCharacteristicProperties', 'BluetoothDevice',
                  'BluetoothRemoteGATTCharacteristic', 'BluetoothRemoteGATTDescriptor', 'BluetoothRemoteGATTServer',
                  'BluetoothRemoteGATTService', 'CaptureController', 'EyeDropper', 'FileSystemDirectoryHandle',
                  'FileSystemFileHandle', 'FileSystemHandle', 'FileSystemWritableFileStream', 'FontData', 'FragmentDirective',
                  'GPU', 'GPUAdapter', 'GPUAdapterInfo', 'GPUBindGroup', 'GPUBindGroupLayout', 'GPUBuffer', 'GPUCanvasContext',
                  'GPUCommandBuffer', 'GPUCommandEncoder', 'GPUCompilationInfo', 'GPUCompilationMessage',
                  'GPUComputePassEncoder', 'GPUComputePipeline', 'GPUDevice', 'GPUDeviceLostInfo', 'GPUError',
                  'GPUExternalTexture', 'GPUInternalError', 'GPUOutOfMemoryError', 'GPUPipelineError', 'GPUPipelineLayout',
                  'GPUQuerySet', 'GPUQueue', 'GPURenderBundle', 'GPURenderBundleEncoder', 'GPURenderPassEncoder',
                  'GPURenderPipeline', 'GPUSampler', 'GPUShaderModule', 'GPUSupportedFeatures', 'GPUSupportedLimits',
                  'GPUTexture', 'GPUTextureView', 'GPUUncapturedErrorEvent', 'GPUValidationError', 'HID', 'HIDConnectionEvent',
                  'HIDDevice', 'HIDInputReportEvent', 'IdentityCredential', 'IdleDetector', 'LaunchParams', 'LaunchQueue',
                  'OTPCredential', 'PaymentAddress', 'PaymentRequest', 'PaymentResponse', 'PaymentMethodChangeEvent',
                  'Presentation', 'PresentationAvailability', 'PresentationConnection', 'PresentationConnectionAvailableEvent',
                  'PresentationConnectionCloseEvent', 'PresentationConnectionList', 'PresentationReceiver',
                  'PresentationRequest', 'Serial', 'SerialPort', 'ToggleEvent', 'USB', 'USBAlternateInterface',
                  'USBConfiguration', 'USBConnectionEvent', 'USBDevice', 'USBEndpoint', 'USBInTransferResult', 'USBInterface',
                  'USBIsochronousInTransferPacket', 'USBIsochronousInTransferResult', 'USBIsochronousOutTransferPacket',
                  'USBIsochronousOutTransferResult', 'USBOutTransferResult', 'WakeLock', 'WakeLockSentinel',
                  'WindowControlsOverlay', 'WindowControlsOverlayGeometryChangeEvent', 'XRAnchor', 'XRAnchorSet',
                  'XRBoundedReferenceSpace', 'XRCPUDepthInformation', 'XRCamera', 'XRDepthInformation', 'XRFrame',
                  'XRHitTestResult', 'XRHitTestSource', 'XRInputSource', 'XRInputSourceArray', 'XRInputSourceEvent',
                  'XRInputSourcesChangeEvent', 'XRLightEstimate', 'XRLightProbe', 'XRPose', 'XRRay', 'XRReferenceSpace',
                  'XRReferenceSpaceEvent', 'XRRenderState', 'XRRigidTransform', 'XRSession', 'XRSessionEvent', 'XRSpace',
                  'XRSystem', 'XRTransientInputHitTestResult', 'XRTransientInputHitTestSource', 'XRView', 'XRViewerPose',
                  'XRViewport', 'XRWebGLDepthInformation', 'XRWebGLLayer', 'AnimationPlaybackEvent', 'AnimationTimeline',
                  'CSSAnimation', 'CSSTransition', 'DocumentTimeline', 'BackgroundFetchManager', 'BackgroundFetchRecord',
                  'BackgroundFetchRegistration', 'BluetoothUUID', 'BrowserCaptureMediaStreamTrack', 'CropTarget',
                  'ContentVisibilityAutoStateChangeEvent', 'DelegatedInkTrailPresenter', 'Ink', 'Highlight',
                  'HighlightRegistry', 'MathMLElement', 'MediaMetadata', 'MediaSession', 'NavigatorUAData', 'Notification',
                  'PaymentManager', 'PaymentRequestUpdateEvent', 'PeriodicSyncManager', 'PermissionStatus', 'Permissions',
                  'PushManager', 'PushSubscription', 'PushSubscriptionOptions', 'RemotePlayback', 'SharedWorker',
                  'SpeechSynthesisErrorEvent', 'SpeechSynthesisEvent', 'SpeechSynthesisUtterance', 'VideoPlaybackQuality',
                  'ViewTransition', 'webkitSpeechGrammar', 'webkitSpeechGrammarList', 'webkitSpeechRecognition',
                  'webkitSpeechRecognitionError', 'webkitSpeechRecognitionEvent', 'n.getGamepads', 'n.javaEnabled',
                  'n.sendBeacon', 'n.vibrate', 'n.canShare', 'n.share', 'n.clearAppBadge', 'n.getBattery', 'n.getUserMedia',
                  'n.requestMIDIAccess', 'n.requestMediaKeySystemAccess', 'n.setAppBadge', 'n.webkitGetUserMedia',
                  'n.getInstalledRelatedApps', 'n.registerProtocolHandler', 'n.unregisterProtocolHandler', 'd.adoptNode',
                  'd.append', 'd.captureEvents', 'd.caretRangeFromPoint', 'd.clear', 'd.close', 'd.createAttribute',
                  'd.createAttributeNS', 'd.createCDATASection', 'd.createComment', 'd.createDocumentFragment',
                  'd.createElement', 'd.createElementNS', 'd.createEvent', 'd.createExpression', 'd.createNSResolver',
                  'd.createNodeIterator', 'd.createProcessingInstruction', 'd.createRange', 'd.createTextNode',
                  'd.createTreeWalker', 'd.elementFromPoint', 'd.elementsFromPoint', 'd.evaluate', 'd.execCommand',
                  'd.exitFullscreen', 'd.exitPictureInPicture', 'd.exitPointerLock', 'd.getElementById',
                  'd.getElementsByClassName', 'd.getElementsByName', 'd.getElementsByTagName', 'd.getElementsByTagNameNS',
                  'd.getSelection', 'd.hasFocus', 'd.importNode', 'd.open', 'd.prepend', 'd.queryCommandEnabled',
                  'd.queryCommandIndeterm', 'd.queryCommandState', 'd.queryCommandSupported', 'd.queryCommandValue',
                  'd.querySelector', 'd.querySelectorAll', 'd.releaseEvents', 'd.replaceChildren', 'd.webkitCancelFullScreen',
                  'd.webkitExitFullscreen', 'd.write', 'd.writeln', 'd.getAnimations', 'd.startViewTransition', 'd.appendChild',
                  'd.cloneNode', 'd.compareDocumentPosition', 'd.contains', 'd.getRootNode', 'd.hasChildNodes',
                  'd.insertBefore', 'd.isDefaultNamespace', 'd.isEqualNode', 'd.isSameNode', 'd.lookupNamespaceURI',
                  'd.lookupPrefix', 'd.normalize', 'd.removeChild', 'd.replaceChild', 'd.addEventListener', 'd.dispatchEvent', 'd.removeEventListener'],
            'E': ['Array'],
            'Infinity': ['Infinity'], 'NaN': ['NaN'], 'u': ['undefined', 'event'], 'Google Inc.': ['n.vendor'],
            'Mozilla': ['n.appCodeName'], 'Netscape': ['n.appName'], self.useragent.lstrip('Mozilla/'): ['n.appVersion'],
            'Win32': ['n.platform'], 'Gecko': ['n.product'], self.useragent: ['n.userAgent'], 'en': ['n.language'], 'en,en-US': ['n.languages'],
            'about:blank': ['d.URL', 'd.documentURI', 'd.referrer'], 'BackCompat': ['d.compatMode'],
            'UTF-8': ['d.characterSet', 'd.charset', 'd.inputEncoding'], 'text/html': ['d.contentType'], 'stake.com': ['d.domain'],
            's': ['d.cookie'], datetime.now().strftime("%m/%d/%Y %H:%M:%S"): ['d.lastModified'], 'complete': ['d.readyState'], 'off': ['d.designMode'],
            'visible': ['d.visibilityState', 'd.webkitVisibilityState'], '': ['d.adoptedStyleSheets'], '#document': ['d.nodeName'],
            'https://stake.com/': ['d.baseURI']
        }
        self.cookie = self.bypass()

    def _get_values(self):
        r = self.client.get(f'https://stake.com/cdn-cgi/challenge-platform/h/g/scripts/jsd/{self.r}/main.js', proxy=self.proxy, cookies=self.cookies,allow_redirects=True)
        key = 'x3MU-7nK0tLQlyRoIXNDZOiPF+c26s$gdJAVzEv9qmapSuh5bwfjHYTk18eWBG4rC'
        for x in r.text.split(';'):
            if len(x) == 65 and '=' not in x:
                key = x
        regex_pattern = r'.*0\.(\d{12,20}):(\d{10}):([a-zA-Z0-9_+*\\-]{43}).*'
        x = re.findall(regex_pattern, r.text)
        s = '0.' + ':'.join(x[0])
        return s, key

    def _get_encrpyted_wb(self, data: dict):
        str_data = json.dumps(data, separators=(',', ':'))
        result = subprocess.run(['node', 'thing.js', str_data, self.key], capture_output=True, text=True)
        wb = result.stdout.strip()
        return wb

    def bypass(self):
        payload = {
            'wp': self._get_encrpyted_wb(self.base_data),
            's': self.s
        }
        r = self.client.post(f'https://stake.com/cdn-cgi/challenge-platform/h/g/jsd/r/{self.r}', proxy=self.proxy, cookies=self.cookies, json=payload)
        console.success("Successfully bypassed cloudflare and got cf_clearance")
        self.cookies.update(r.cookies)
        return self.cookies

class Turnstile:
    def __init__(self, sitekey:str=None, rqdata=None, captchaService=captchaService,proxy=None,iua=False) -> None:
        self.captchaService = captchaService
        self.rqdata = rqdata
        self.proxy = proxy
        self.iua = iua
        self.sitekey = sitekey

    def createTask(self):
        if self.captchaService == "capsolver" or self.captchaService == "capmonster":
            if self.captchaService == "capsolver":
                payload = {
                    "clientKey": capApiKey,
                    "task": {
                        "type": "AntiCloudflareTask",
                        "websiteURL": "https://stake.com/?tab=register&modal=auth",
                        "websiteKey": "0x4AAAAAAAGD4gMGOTFnvupz"
                    },
                    "proxy": self.proxy

                    } if not self.iua else {
                    "clientKey": capApiKey,
                    "task": {
                            "type": "AntiCloudflareTask",
                            "websiteURL": "https://stake.com/",
                            "proxy": self.proxy
                        }
                    }
            else:
                payload = {
                    "clientKey": capApiKey,
                    "task": {
                        "type": "TurnstileTaskProxyless",
                        "websiteURL": "https://stake.com/?tab=register&modal=auth",
                        "websiteKey": "0x4AAAAAAAGD4gMGOTFnvupz"
                    }
                    }
            request = ss.post(f"https://api.{'capmonster.cloud' if self.captchaService == 'capmonster' else 'capsolver.com'}/createTask", headers={"content-type":"application/json"}, json=payload)
            return request.json()["taskId"]
        
    def getTaskResult(self, taskId):
        if self.captchaService == "capsolver" or self.captchaService == "capmonster":
            request = ss.post("https://api.capsolver.com/getTaskResult" if self.captchaService == "capsolver" else "https://api.capmonster.cloud/getTaskResult",json={"clientKey":capApiKey,"taskId": taskId})
            if request.status_code in [200,201,202,203,204,205]:
                js = request.json()
                if js["status"] == "ready" and js["errorId"] == 0:
                    token = js["solution"]["token"]
                    return token
                else:
                    return False
            else:
                console.warn(f"Failed to solve captcha [Status Code : {request.status_code} Text: {request.text}]",t=1)

    def solve_captcha(self):
        t = time.time()
        taskId = self.createTask()
        while True:
            token = self.getTaskResult(taskId)
            t = time.time()-t
            if token:
                console.success(f"Successfully solved captcha '[{token[:18]}]' in {str(t)[:5]}s")
                return token

class Mail:
    def __init__(self,password=None,username=None):
        self.headers={
            "accept":"application/ld+json",
            "Origin":"https://mail.tm",
            "Referer":"https://mail.tm/",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
        self.ss = ss

    def get_domain(self) -> str:
        domains = self.ss.get("https://api.mail.tm/domains",headers=self.headers)
        return random.choice(domains.json()["hydra:member"])["domain"]
    
    def get_account(self) -> dict:
        while True:
            domain = self.get_domain()
            password = self.generatePassword()
            username = self.generateUsername2()
            account = self.ss.post("https://api.mail.tm/accounts",headers=self.headers,json={"address":username+f"@{domain}","password": password})
            if "Internal Server Error" in account.text:
                password = ''.join([random.choice(string.ascii_letters + string.digits + "!.") for i in range(10)])
                account = self.ss.post("https://api.mail.tm/accounts",headers=self.headers,json={"address":username+f"@{domain}","password": password})
                break
            if "This value is already used." in account.text:
                username = f'{self.generateUsername()}'+''.join([random.choice(string.digits+string.ascii_lowercase) for i in range(10)])
                account = self.ss.post("https://api.mail.tm/accounts",headers=self.headers,json={"address":username+f"@{domain}","password": password})
                break
            if account.status_code in [201,200,203,202]:
                account = account.json()
                account.update({"password": password})
                return account
            else:
                self.get_account()

    def generateUsername2(self):
        return f'{self.generateUsername()}'+''.join([random.choice(string.digits+string.ascii_lowercase) for i in range(10)])
    
    def generatePassword(self):
        return ''.join([random.choice(string.ascii_letters + string.digits + "!.") for i in range(10)])
    
    def get_token(self) -> str:
        try:
            headers = self.headers
            account = self.get_account()
            token = self.ss.post("https://api.mail.tm/token",headers=self.headers,json={"address":account["address"],"password":account["password"]}).json()["token"]
            headers.update({"authorization":f"Bearer {token}"})
            return (token, account)
        except:
            self.get_token()

    def get_messages(self, token) -> dict:
        headers = self.headers
        headers.update({"authorization":"Bearer "+token})
        messages = self.ss.get("https://api.mail.tm/messages",headers=headers)
        return (messages.json(), headers)
    
    def get_messages_items(self, token):
        messages, headers = self.get_messages(token)
        if "hydra:totalItems" in str(messages):
            items = messages["hydra:totalItems"]
            if items >= 1:
                return (True,messages, headers)
        if "hydra:totalItems" not in str(messages):
            return (True,messages, headers)
        else:
            return (False,messages, headers)
        
    def wait_messages(self, token, interval=None) -> dict:
        if not interval:
            while True:
                try:
                    result, messages, headers = self.get_messages_items(token)
                    if result:
                        message =  messages["hydra:member"][0]
                        return self.get_message(message["id"], headers)
                    time.sleep(1)
                except:
                    pass
        else:
            for i in range(interval):
                time.sleep(1)
                try:
                    result, messages, headers = self.get_messages_items(token)
                    if result:
                        message =  messages["hydra:member"][0]
                        return self.get_message(message["id"], headers)
                except:
                    pass

    def get_message(self, messageId, headers):
        message = self.ss.get(f"https://api.mail.tm/messages/{messageId}", headers=headers).json()["text"]
        return message
    
    def generateUsername(self):
        request = ss.get("https://randomuser.me/api/?inc=login")
        if request.status_code in [200,201,203,205,202,204]:
            js = request.json()
            username = js["results"][0]["login"]["username"]
            return username
        else:
            print(request.text)
            return ''.join([random.choice(string.ascii_lowercase) for x in range(10)])
        
    def create_email(self):
        token, account = self.get_token()
        account =  f"{account['address']}:{account['password']}"
        console.success(f"Created email {account}")
        return (token, account)
    
class Utils:
    def __init__(self) -> None:
        pass

    def reformatProxies(self,proxy:str):
        if len(proxy.split(":")) == 3 or len(proxy.split(":")) == 4:
            if "://" in proxy:
                protocol = proxy.split("://")[0]
            else:
                protocol = None
            credentials,proxyInfo = proxy.split("@")
            if protocol:
                credentials = credentials.split("://")[1]
            username,password = credentials.split(":")
            host,port = proxyInfo.split(":")
            return f"{protocol}:{host}:{port}:{username}:{password}"
        else:
            return proxy
        
    def getVerifyUrl(self, text:str):
        found = False
        for line in text:
            if found:
                line = line.replace("[", "")
                line = line.replace("]", "")
                return line
            if "Verify Email" in line:
                found = True

    def save(self, account):
        with open("tokens.txt","a") as f:
            f.write(account+"\n")
            f.close()

    def genProxy(self):
        return random.choice(proxies)
    
class Script:
    def __init__(self) -> None:
        self.utils = Utils()
        self.captcha = Turnstile()
        self.email = Mail()
    def mailVerify(self, requests, url:str, proxy):
        url = url.replace("http://","https://")
        request = ss.get(url, allow_redirects=True)
        url = request.url
        request = requests.get(url, proxy=proxy)
        if request.status_code in [200,201,202,203,204,205]:
            console.success("Successfully mail verified.")
            return True
        else:
            console.warn(f"Failed to mail verify.. | Status Code : {request.status_code}",t=1)
            
    def gen(self):
        global timeouted
        global generated
        global failed
        requests = tls_client.Session(client_identifier="chrome120",random_tls_extension_order=True)
        requests.headers["User-Agent"] = UserAgent
        proxy = f"http://{self.utils.genProxy()}" if proxyType == "http" else f"https://{self.utils.genProxy()}"
        cookies = {}
        main = requests.post("https://stake.com/?tab=register&modal=auth", proxy=proxy)
        cookies.update(main.cookies)
        fail = False
        t1 = time.time()
        email = self.email
        try:
            emailToken, emailAccount = email.create_email()
        except:
            console.warn("Failed to create email inbox genning without email !",t=1)
            emailAccount = f"{email.generateUsername2()}:{email.generatePassword()}"
            fail = True
        emailUsername, emailPassword = emailAccount.split(":")
        capToken = self.captcha.solve_captcha()
        headers = {
            'authority': 'stake.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'access-control-allow-origin': '*',
            'content-type': 'application/json',
            'origin': 'https://stake.com',
            'referer': 'https://stake.com/?tab=register&modal=auth',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'x-language': 'en',
        }
        payload = {
            'query': 'mutation RegisterUser($name: String!, $password: String!, $email: String!, $turnstileToken: String!, $sessionName: String!, $code: String, $signupCode: String, $blackbox: String, $dob: Date!, $clickId: String) {\n  registerUser(\n    name: $name\n    password: $password\n    email: $email\n    turnstileToken: $turnstileToken\n    code: $code\n    signupCode: $signupCode\n    sessionName: $sessionName\n    blackbox: $blackbox\n    dob: $dob\n    clickId: $clickId\n  ) {\n    ...UserAuthenticatedSession\n  }\n}\n\nfragment UserAuthenticatedSession on UserAuthenticatedSession {\n  token\n  session {\n    ...UserSession\n    user {\n      ...UserAuth\n    }\n  }\n}\n\nfragment UserSession on UserSession {\n  id\n  sessionName\n  ip\n  country\n  city\n  active\n  updatedAt\n}\n\nfragment UserAuth on User {\n  id\n  name\n  email\n  hasPhoneNumberVerified\n  hasEmailVerified\n  hasPassword\n  intercomHash\n  createdAt\n  hasTfaEnabled\n  mixpanelId\n  hasOauth\n  isMaxBetEnabled\n  isReferred\n  isSportsbookExcluded\n  registeredWithVpn\n  flags {\n    flag\n    createdAt\n  }\n  signupCode {\n    code {\n      code\n    }\n  }\n  roles {\n    name\n  }\n  balances {\n    ...UserBalance\n  }\n  activeClientSeed {\n    id\n    seed\n  }\n  previousServerSeed {\n    id\n    seed\n  }\n  activeDepositBonus {\n    status\n    minDepositValue\n    maxDepositValue\n    maxBetMultiplier\n    bonusMultiplier\n    expectedAmountMultiplier\n  }\n  activeServerSeed {\n    id\n    seedHash\n    nextSeedHash\n    nonce\n    blocked\n  }\n  veriffStatus\n  verifications {\n    userVerification {\n      ...UserVerification\n    }\n    ageVerification {\n      ...AgeVerification\n    }\n    addressVerification {\n      ...AddressVerification\n    }\n    documentVerification {\n      ...DocumentVerification\n    }\n    riskVerification {\n      ...RiskVerification\n    }\n    employmentVerification {\n      ...EmploymentVerification\n    }\n  }\n  termsOfService {\n    status\n  }\n  veriffBiometricVerificationStatus\n  notificationCount\n  currentPlaySession {\n    fitToPlay\n  }\n}\n\nfragment UserBalance on UserBalance {\n  available {\n    amount\n    currency\n  }\n  vault {\n    amount\n    currency\n  }\n}\n\nfragment UserVerification on IdentityUserVerification {\n  status\n  verified\n}\n\nfragment AgeVerification on IdentityAgeVerification {\n  id\n  active\n  birthDate\n  createdAt\n  expireAt\n  type\n  user {\n    id\n    name\n  }\n  verified\n}\n\nfragment AddressVerification on IdentityAddressVerification {\n  active\n  city\n  country\n  createdAt\n  expireAt\n  id\n  state\n  street\n  type\n  user {\n    id\n    name\n  }\n  verified\n  zip\n}\n\nfragment DocumentVerification on IdentityDocumentVerification {\n  active\n  createdAt\n  documentBirthDate\n  documentCity\n  documentCountry\n  documentExpiry\n  documentFirstName\n  documentId\n  documentLastName\n  documentNationality\n  documentState\n  documentStreet\n  documentType\n  documentZip\n  expireAt\n  id\n  type\n  user {\n    id\n    name\n  }\n  verified\n}\n\nfragment RiskVerification on IdentityRiskVerification {\n  active\n  createdAt\n  expireAt\n  id\n  nationalityCountry\n  nonPoliticallyExposed\n  nonThirdPartyAccount\n  preferredName\n  type\n  user {\n    id\n    name\n  }\n  verified\n}\n\nfragment EmploymentVerification on IdentityEmploymentVerification {\n  active\n  createdAt\n  employerCity\n  employerCountry\n  employerName\n  employerPhone\n  employerState\n  employerStreet\n  employerZip\n  expireAt\n  id\n  type\n  user {\n    id\n    name\n  }\n  verified\n  occupation\n}\n',
            'variables': {
                'browser': 'Chrome',
                'browserVersion': '120',
                'os': 'Windows',
                'email': emailUsername,
                'name': emailUsername.split("@")[0],
                'password': emailPassword,
                'dob': '1/6/2000',
                'turnstileToken': capToken,
                'sessionName': 'Chrome (Unknown)',
                'blackbox': '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;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',
            },
        }
        request = requests.post("https://stake.com/_api/graphql", headers=headers, json=payload, proxy=proxy, cookies=cookies)
        if request.status_code in [200,201,202,203,204,205]:
            generated += 1
            ctypes.windll.kernel32.SetConsoleTitleW(title.format(generated,failed,timeouted))
            try:
                js = request.json()["data"]["registerUser"]
            except:
                try:
                    js = json.loads(request.text)
                except:
                    print(request.text)
            t1 = time.time()-t1
            console.success(f"Successfully created account {js['session']['user']['name']} => {js['token'][:17]}******* in {str(t1)[:5]}{', verifying the account....' if not fail and confirmVerification else ''}")
            if not fail and confirmVerification:
                try:
                    console.warn("Waiting for verify url...")
                    verifyUrl = self.utils.getVerifyUrl(text=email.wait_messages(emailToken, interval=60).splitlines())
                    mailVerified = self.mailVerify(url=verifyUrl, requests=requests, proxy=proxy)
                except:
                    console.warn("Failed to mail verify retry 1 more time...",t=1)
                    try:
                        verifyUrl = self.utils.getVerifyUrl(text=email.wait_messages(emailToken, interval=60).splitlines())
                        mailVerified = self.mailVerify(url=verifyUrl, requests=requests, proxy=proxy)
                    except:
                        mailVerified = False
            else:
                mailVerified = False
            if mailVerified:
                self.utils.save(f"{emailUsername}:{emailPassword}:{js['token']} | Mail verified")
                return True
            if not confirmVerification:
                self.utils.save(f"{emailUsername}:{emailPassword}:{js['token']} | Mail unverified")
                return True
            if not fail:
                self.utils.save(f"{emailUsername}:{emailPassword}:{js['token']} | Failed to verify using email")
                return True
            else:
                self.utils.save(f"{emailUsername}@failed.nodomain:{emailPassword}:{js['token']} | Failed to create email info : the token is working. (you can access the account and change email to a working one the password is valid)")
                return True
        if request.status_code == 429:
            timeouted += 1
            ctypes.windll.kernel32.SetConsoleTitleW(title.format(generated,failed,timeouted))
            console.warn("Failed to create account due to ratelimit !",t=1)
            return False
        if request.status_code > 400 and request.status_code < 500:
            failed += 1
            ctypes.windll.kernel32.SetConsoleTitleW(title.format(generated,failed,timeouted))
            console.warn(f"Failed to create account due to cloudflare | Status Code : {request.status_code}",t=1)
            return False
        else:
            failed += 1
            ctypes.windll.kernel32.SetConsoleTitleW(title.format(generated,failed,timeouted))
            console.warn(f"Failed to create account | Status Code : {request.status_code}",t=1)
            return False
        
script = Script()
def startConcurrent():
    with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS) as executor:
        while True:
            results = [executor.submit(script.gen) for i in range(10)]

def startThreading():
    while True:
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=script.gen, args=())
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

def start():
    while True: 
        script.gen()

def main():
    if THREADS == 1 or THREADS == 0:
        start()
    else:
        startConcurrent()

main()