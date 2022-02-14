from mindmeld.components.nlp import NaturalLanguageProcessor

nlp = NaturalLanguageProcessor(app_path='smiddle_products')
erc = nlp.domains['products'].intents['specify_product'].entity_recognizer
ers = nlp.domains['products'].intents['specify_product'].get_entity_processors()['product'].entity_resolver
erc.fit()
ers.fit()

def detect_product(state):
    def _state(request, responder):
        eq = erc.predict(request.text)
        if eq:
            product = eq[0]
            entities = ers.predict(product.entity.text)
            if entities and entities[0]['score'] > 30:
                print(entities[0]['cname'])
                responder.frame['interested_in'] = entities[0]['cname']
        # products = [e['value'][0]['cname'] for e in request.entities if e['type'] == 'product']
        # if products:
        #     responder.frame['interested_in'] = products[0]  # TODO: Easy multyproduct
        state(request, responder)

    _state.__name__ = state.__name__
    return _state