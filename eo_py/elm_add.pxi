

cimport elm_add

def elm_run():
   elm_add.elm_run()


def elm_init(argv):
    cdef void *p
#    s = " ".join(argv)
#    cdef char *cstr
#    cdef char **p_cstr
#    cstr = <char*>s
#    print "cstr = ", cstr
#    c_csrt = <char**>cstr
#    print "p_cstr[0] = ", p_cstr[0]
    p = NULL
    return <int>(elm_add.elm_init(len(argv), NULL))

