from abc import abstractmethod

import pika, json


class QueueBuilder:
    def __init__(self):
        self.__host = None
        self.__port = None
        self.__username = None
        self.__password = None
        self.__exchange = None

    def host(self, host: str):
        self.__host = host

    def port(self, port: int):
        self.__port = port

    def username(self, username: str):
        self.__username = username

    def password(self, password: str):
        self.__password = password

    def exchange(self, exchange: str):
        self.__exchange = exchange

    def build(self):
        return QueueInformation(
            self.__host,
            self.__port,
            self.__username,
            self.__password,
            self.__exchange)


class QueueBuilderSpec:
    def __init__(self, builder: QueueBuilder):
        self._builder = builder


class QueueExchange(QueueBuilderSpec):
    def __init__(self, builder: QueueBuilder):
        super().__init__(builder)

    def exchange(self, exchange: str):
        self._builder.exchange(exchange)
        return self._builder


class QueuePassword(QueueBuilderSpec):
    def __init__(self, builder: QueueBuilder):
        super().__init__(builder)

    def password(self, password: str):
        self._builder.password(password)
        return QueueExchange(self._builder)


class QueueUsername(QueueBuilderSpec):
    def __init__(self, builder: QueueBuilder):
        super().__init__(builder)

    def username(self, username: str):
        self._builder.username(username)
        return QueuePassword(self._builder)


class QueuePort(QueueBuilderSpec):
    def __init__(self, builder: QueueBuilder):
        super().__init__(builder)

    def port(self, port: int):
        self._builder.port(port)
        return QueueUsername(self._builder)


class QueueHost(QueueBuilderSpec):
    def __init__(self, builder: QueueBuilder):
        super().__init__(builder)

    def host(self, host: str):
        self._builder.host(host)
        return QueuePort(self._builder)


class QueueInformation:
    def __init__(self, host, port, username, password, exchange):
        self.__host = host
        self.__port = port
        self.__username = username
        self.__password = password
        self.__exchange = exchange

    def host(self):
        return self.__host

    def port(self):
        return self.__port

    def username(self):
        return self.__username

    def password(self):
        return self.__password

    def exchange(self):
        return self.__exchange

    @staticmethod
    def builder():
        builder = QueueBuilder()
        return QueueHost(builder)


class Publisher:
    def __init__(self, information: QueueInformation):
        self._queue = information

    @abstractmethod
    def _connect_(self):
        pass

    @abstractmethod
    def publish(self, routing_key, payload):
        pass


class RabbitPublisher(Publisher):
    def __init__(self, information: QueueInformation):
        super().__init__(information)
        self._connect_()

    def __enter__(self):
        return RabbitPublisher(self._queue)

    def _connect_(self):
        credentials = pika.credentials.PlainCredentials(self._queue.username(), self._queue.password())
        connection_parameter = pika.ConnectionParameters(
            host=self._queue.host(),
            port=self._queue.port(),
            credentials=credentials)
        self.__connection = pika.BlockingConnection(connection_parameter)
        self.__channel = self.__connection.channel()

    def publish(self, routing_key, payload, headers=None):
        properties = None
        if headers is not None:
            properties = pika.BasicProperties(headers=headers)
        self.__channel.basic_publish(
            exchange=self._queue.exchange(),
            routing_key=routing_key,
            body=payload,
            properties=properties)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__channel.close()
        self.__connection.close()


class Consumer:
    def __init__(self, information: QueueInformation):
        self._queue = information

    @abstractmethod
    def _connect_(self):
        pass

    @abstractmethod
    def consume(self):
        pass




class RabbitConsumer(Consumer):
    def __init__(self, information: QueueInformation):
        super().__init__(information)
        self._connect_()

    def __enter__(self):
        return RabbitConsumer(self._queue)

    def _connect_(self):
        credentials = pika.credentials.PlainCredentials(self._queue.username(), self._queue.password())
        connection_parameter = pika.ConnectionParameters(
            host=self._queue.host(),
            port=self._queue.port(),
            credentials=credentials)
        self.__connection = pika.BlockingConnection(connection_parameter)
        self.__channel = self.__connection.channel()

    def callback(self, ch, method, properties, body):
        data = json.loads(body)
        #print("iter:", data['iter'])
        self.response = data['iter']
        ch.stop_consuming()

    
    def consume(self, queuename):
        #properties = None
        #if headers is not None:
        #    properties = pika.BasicProperties(headers=headers)
        self.__channel.basic_consume(
            queuename,
            on_message_callback=self.callback,
            auto_ack = True)
        self.__channel.start_consuming()
        return int(self.response)
        #time.sleep(5)
        #self.__channel.stop_consuming()


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__channel.close()
        self.__connection.close()
