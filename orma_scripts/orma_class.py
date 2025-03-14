# ORMA is a model analysis based on OpenRefine JSON recipe
# It reveal dependencies between operations
# levels of operations based on affect :
'''
level 0: no change
level 1: only change content
level 2: only change dependency
level 3: both change dependency and content
'''
from orma import parallel_view_main
from orma_scripts.module_view import split_recipe
from orma_scripts.schema_view import model_schema_evolution
from orma_scripts.table_view import generate_table_dot


class ORMA:
    def __init__(self):
        """
          Init functions for this class, put any initialization attributes
          that you need here
          """
        pass

    @staticmethod
    def generate_table_view(project_id, output, combined=False):
        generate_table_dot(project_id, output, combined)

    @staticmethod
    def generate_parallel_view(project_id, output_gv):
        parallel_view_main(project_id, output_gv)

    @staticmethod
    def generate_schema_view(project_id, output_gv):
        model_schema_evolution(project_id=project_id, output_gv=output_gv)

    @staticmethod
    def generate_module_views(project_id, output_gv):
        split_recipe(project_id=project_id, output_gv=output_gv)


class ORMAProcessor:
    def __init__(self):
        pass

    def generate_views(self, project_id, output, type="table_view", combined=False, **kwargs):
        if type == "table_view":
            if combined:
                return ORMA.generate_table_view(project_id, output, combined)
            else:
                return ORMA.generate_table_view(project_id, output, **kwargs)
        elif type == "schema_view":
            return ORMA.generate_schema_view(project_id, output)
        elif type == "parallel_view":
            return ORMA.generate_parallel_view(project_id, output)
        elif type == 'modular_views':
            return ORMA.generate_module_views(project_id, output)
        else:
            raise BaseException("Workflow type Only Serial, Parallel or Merge")


if __name__ == '__main__':
    # ORMAProcessor().generate_views(2494992270641, 'usecase2/table_view/table_view.gv',
    #                                'table_view')
    # ORMAProcessor().generate_views(2494992270641, 'usecase2/schema_view/schema_view.gv',
    #                                'schema_view')
    # ORMAProcessor().generate_views(2494992270641, 'usecase2/parallel_view/parallel_view.gv',
    #                                'parallel_view')
    # ORMAProcessor().generate_views(1998304485672, 'gemma_p60',
    #                                "parallel_view")
    # ORMAProcessor().generate_views(1831783871747, 'mistral_p60',
    #                                "parallel_view")
    # ORMAProcessor().generate_views(2669592531117, 'llama_p60',
    #                             "parallel_view")
    
    ORMAProcessor().generate_views(2011536917259, 'user1',
                            "parallel_view")
    # split_recipe(project_id=2494992270641)
    # cluster_main(project_id=2494992270641) usecase2/modular_views/parallel_view
    # split_recipe()
    # generate_table_dot()  # table_view
    # model_schema_evolution(project_id=2124203262743, output_gv='output/schema_view.gv') # summary view
    # main1()  # modular_views
    # main()
    # temp(2124203262743)
