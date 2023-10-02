from metaflow import FlowSpec, step, Parameter

# Welcome to your first Metaflow flow!
# To run locally: python $HOME/flows/hello_flow.py run
# To run on kubernetes: python $HOME/flows/hello_flow.py --with kubernetes run
class HelloFlow(FlowSpec):
    @step
    def start(self):
        print("Welcome to your first flow!")
        self.next(self.end)

    @step
    def end(self):
        pass


if __name__ == "__main__":
    HelloFlow()
